TRABALHO – TPI: Coloração de Grafos
===================================

Instruções de compilação e execução
Ambiente: UNIX / LINUX (WSL Ubuntu recomendado)

-----------------------------------------------
1. PRÉ-REQUISITOS
-----------------------------------------------
• Python 3.10 instalado
• IBM CPLEX Studio instalado (ex.: /opt/ibm/ILOG/CPLEX_Studio2211)
• Módulo Python docplex instalado
• Arquivo solve_coloring.py na pasta do trabalho
• Instâncias TPI_COL_1.txt, TPI_COL_2.txt, TPI_COL_3.txt

-----------------------------------------------
2. CONFIGURAÇÃO DO AMBIENTE
-----------------------------------------------

Antes de executar o solver, exportar o caminho do CPLEX:

    export PYTHONPATH=/opt/ibm/ILOG/CPLEX_Studio2211/cplex/python/3.10/x86-64_linux:$PYTHONPATH

Testar:

    python3.10 - << 'PY'
    import cplex
    from docplex.mp.model import Model
    print("CPLEX e docplex carregados com sucesso!")
    PY

-----------------------------------------------
3. EXECUÇÃO DO SOLVER
-----------------------------------------------

Resolver uma instância:

    python3.10 solve_coloring.py TPI_COL_1.txt

Resolver com limite de tempo:

    python3.10 solve_coloring.py TPI_COL_2.txt --time-limit 120

Executar todas as instâncias:

    chmod +x run_all_coloring.sh
    ./run_all_coloring.sh

-----------------------------------------------
4. FORMATO DA SAÍDA
-----------------------------------------------

Cada execução gera:

    sol_TPI_COL_X.txt

Conteúdo do arquivo:

• instance: <nome>
• num_colors: <menor número de cores encontrado>
• assignments: lista vértice → cor

-----------------------------------------------
5. RESULTADOS OBTIDOS
-----------------------------------------------

Instância TPI_COL_1.txt:
num_colors = 4

Instância TPI_COL_2.txt:
num_colors = 42

Instância TPI_COL_3.txt:
num_colors = 5

-----------------------------------------------
6. OBSERVAÇÕES FINAIS
-----------------------------------------------
• A modelagem utiliza variáveis x(v,k) e y(k).
• O CPLEX encontra a coloração mínima via MIP.
• Todas as execuções foram feitas em Linux (WSL Ubuntu).
