#!/usr/bin/env python3.10
# solve_coloring.py
# Modelo de coloração usando CPLEX/docplex

import sys
import os
from glob import glob
import argparse

from docplex.mp.model import Model


def read_instance(path):
    edges = []
    n = None
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith(('c', '%', '#')):
                continue
            parts = line.split()
            if parts[0] == 'p':
                n = int(parts[2])
            elif parts[0] == 'e':
                u = int(parts[1]); v = int(parts[2])
                edges.append((u, v))
    if n is None:
        raise ValueError("Instância sem linha 'p edge n m'")
    return n, edges


def build_and_solve(path, time_limit=None, mip_gap=None, print_model=False):
    n, edges = read_instance(path)
    K = n  # máximo de cores

    model = Model(name=os.path.basename(path))

    y = {k: model.binary_var(name=f"y_{k}") for k in range(1, K+1)}
    x = {(v,k): model.binary_var(name=f"x_{v}_{k}") for v in range(1,n+1) for k in range(1,K+1)}

    # objetivo — minimizar número de cores
    model.minimize(model.sum(y[k] for k in y))

    # cada vértice recebe 1 cor
    for v in range(1, n+1):
        model.add_constraint(model.sum(x[(v,k)] for k in range(1,K+1)) == 1)

    # vértices adjacentes não podem ter mesma cor
    for (u,v) in edges:
        for k in range(1, K+1):
            model.add_constraint(x[(u,k)] + x[(v,k)] <= 1)

    # x <= y
    for v in range(1,n+1):
        for k in range(1,K+1):
            model.add_constraint(x[(v,k)] <= y[k])

    # quebra de simetria
    for k in range(1, K):
        model.add_constraint(y[k] >= y[k+1])

    if time_limit:
        model.parameters.timelimit = time_limit
    if mip_gap:
        model.parameters.mip.tolerances.mipgap = mip_gap

    if print_model:
        model.export_as_lp("model.lp")

    print(f"Solving {path}...")
    sol = model.solve(log_output=True)

    solname = "sol_" + os.path.splitext(os.path.basename(path))[0] + ".txt"

    with open(solname, "w") as f:
        f.write(f"instance: {path}\n")
        if sol is None:
            f.write("status: infeasible\n")
            return
        f.write(f"num_colors: {int(model.objective_value)}\n")
        f.write("assignments:\n")
        for v in range(1,n+1):
            for k in range(1,K+1):
                if abs(x[(v,k)].solution_value - 1) < 1e-6:
                    f.write(f"{v} {k}\n")
                    break

    print(f"Solução salva em {solname}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("inputs", nargs="+")
    parser.add_argument("--time-limit", type=int)
    parser.add_argument("--mip-gap", type=float)
    parser.add_argument("--print-model", action="store_true")
    args = parser.parse_args()

    files = []
    for p in args.inputs:
        files.extend(glob(p))

    for fpath in files:
        build_and_solve(fpath, time_limit=args.time_limit, mip_gap=args.mip_gap, print_model=args.print_model)


if __name__ == "__main__":
    main()
