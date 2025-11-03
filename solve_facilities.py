#!/usr/bin/env python3.10
"""
solve_facilities.py

Uso:
    python3.10 solve_facilities.py <instancia.txt>
    python3.10 solve_facilities.py pasta_com_instancias/*.txt

O script:
- Lê a(s) instância(s) no formato:
    ni nj c Q NL
    i j g_ij p_ij
    ...
- Monta um MIP:
    y_i in {0,1} abrir facilidades
    x_ij in {0,1} cliente j atendido por i (apenas pares listados)
    min sum_i c*y_i + sum_{i,j} g_ij * x_ij
    s.t. cada cliente j atendido exatamente 1 vez
         sum_j p_ij * x_ij <= Q * y_i  (capacidade)
- Resolve com docplex (CPLEX como backend).
- Imprime resumo e grava arquivo sol_<instancia>.txt
"""
import sys
import os
from glob import glob
from collections import defaultdict
import argparse

try:
    from docplex.mp.model import Model
except Exception as e:
    print("ERRO: não foi possível importar docplex. Verifique se instalou com python3.10.")
    print("Instale com: sudo python3.10 -m pip install docplex")
    raise

def read_instance(path):
    toks = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = line.split()
            toks.extend(parts)
    if len(toks) < 5:
        raise ValueError(f"Arquivo {path} com formato inválido (menos de 5 tokens).")
    ni = int(toks[0]); nj = int(toks[1]); c = float(toks[2]); Q = float(toks[3]); NL = int(toks[4])
    rem = toks[5:]
    expected = NL * 4
    if len(rem) < expected:
        raise ValueError(f"Arquivo {path}: esperado {expected} tokens de entradas, achados {len(rem)}")
    entries = []
    idx = 0
    for _ in range(NL):
        i = int(rem[idx]); j = int(rem[idx+1])
        g = float(rem[idx+2]); p = float(rem[idx+3])
        entries.append((i, j, g, p))
        idx += 4
    return ni, nj, c, Q, entries

def build_and_solve(path, time_limit=None, mip_gap=None, print_model=False):
    ni, nj, c, Q, entries = read_instance(path)
    # map pairs
    pairs = {(i,j): (g,p) for (i,j,g,p) in entries}
    # create model
    model = Model(name=os.path.basename(path))
    # variables
    y = {i: model.binary_var(name=f"y_{i}") for i in range(1, ni+1)}
    x = {}
    for (i,j),(g,p) in pairs.items():
        x[(i,j)] = model.binary_var(name=f"x_{i}_{j}")

    # objective
    obj = model.sum(c * y[i] for i in y) + model.sum(pairs[(i,j)][0] * x[(i,j)] for (i,j) in x)
    model.minimize(obj)

    # constraints: each client assigned exactly once
    for j in range(1, nj+1):
        assigns = [x[(i,j)] for i in range(1, ni+1) if (i,j) in x]
        if len(assigns) == 0:
            # infeasible instance: no facility can serve client j
            model.add_constraint(0 == 1, ctname=f"assign_client_{j}_impossible")
        else:
            model.add_constraint(model.sum(assigns) == 1, ctname=f"assign_client_{j}")

    # capacity constraints
    for i in range(1, ni+1):
        terms = [pairs[(i,j)][1] * x[(i,j)] for j in range(1, nj+1) if (i,j) in x]
        if terms:
            model.add_constraint(model.sum(terms) <= Q * y[i], ctname=f"cap_fac_{i}")
        else:
            # facility never used; constraint trivial but keep it
            model.add_constraint(0 <= Q * y[i], ctname=f"cap_fac_{i}_trivial")

    # parameters
    if time_limit is not None:
        model.parameters.timelimit = time_limit
    if mip_gap is not None:
        model.parameters.mip.tolerances.mipgap = mip_gap

    # optionally print model to LP file for debugging
    lpfile = None
    if print_model:
        lpfile = os.path.splitext(os.path.basename(path))[0] + ".lp"
        model.export_as_lp(lpfile)
        print(f"Modelo exportado para {lpfile}")

    # solve
    print(f"Solving {path} — ni={ni}, nj={nj}, lines={len(entries)}, c={c}, Q={Q}")
    sol = model.solve(log_output=True)
    out = {}
    if sol is None:
        print("Nenhuma solução encontrada (infeasible or time limit).")
        status = model.get_solve_status()
        print("Status:", status)
        out['status'] = status
    else:
        objval = model.objective_value
        out['objective'] = objval
        out['open_facilities'] = [i for i in y if abs(y[i].solution_value - 1.0) < 1e-6]
        out['assignments'] = [(i,j) for (i,j) in x if abs(x[(i,j)].solution_value - 1.0) < 1e-6]
        print(f"Objetivo = {objval:.6f}")
        print("Facilidades abertas:", out['open_facilities'])
        print("Atribuições (i,j):", out['assignments'])

    # write solution file
    solname = "sol_" + os.path.splitext(os.path.basename(path))[0] + ".txt"
    with open(solname, 'w') as f:
        f.write(f"instance: {path}\n")
        f.write(f"status: {out.get('status','ok')}\n")
        if 'objective' in out:
            f.write(f"objective: {out['objective']:.6f}\n")
        f.write("open_facilities:\n")
        for i in out.get('open_facilities',[]):
            f.write(f"{i}\n")
        f.write("assignments:\n")
        for (i,j) in out.get('assignments',[]):
            f.write(f"{i} {j}\n")
    print(f"Solução escrita em {solname}")
    return out

def main():
    parser = argparse.ArgumentParser(description="Resolve instância(s) do problema de facilidades com docplex (CPLEX backend).")
    parser.add_argument("inputs", nargs='+', help="arquivos .txt ou curinga (ex: pasta/*.txt)")
    parser.add_argument("--time-limit", type=int, default=None, help="time limit em segundos")
    parser.add_argument("--mip-gap", type=float, default=None, help="mip gap (ex: 0.0001)")
    parser.add_argument("--print-model", action='store_true', help="exporta modelo .lp para debug")
    args = parser.parse_args()

    files = []
    for pattern in args.inputs:
        files.extend(sorted(glob(pattern)))
    if not files:
        print("Nenhum arquivo encontrado para os padrões informados.")
        sys.exit(1)

    for fpath in files:
        try:
            build_and_solve(fpath, time_limit=args.time_limit, mip_gap=args.mip_gap, print_model=args.print_model)
        except Exception as e:
            print("Erro ao resolver", fpath, ":", e)

if __name__ == "__main__":
    main()
