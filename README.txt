Trabalho – Uso do CPLEX via Python
Disciplina: Programação Linear-Inteira
Aluno: Victor Albino

------------------------------------------------------------
INSTRUÇÕES DE COMPILAÇÃO E EXECUÇÃO (AMBIENTE LINUX/UNIX)
------------------------------------------------------------

1. Pré-requisitos:
   - Sistema operacional: Ubuntu (WSL ou nativo)
   - Python 3.10 instalado
   - IBM ILOG CPLEX Studio instalado (ex.: /opt/ibm/ILOG/CPLEX_Studio2211)
   - Pacote docplex instalado para Python:
     sudo python3.10 -m pip install docplex

2. Estrutura de arquivos:
   - solve_facilities.py      → script principal (modelo em Python)
   - run_all.sh               → script para rodar várias instâncias
   - TPI_F_0.txt, TPI_F_1.txt, TPI_F_2.txt → instâncias fornecidas pelo professor

3. Execução de uma instância:
   python3.10 solve_facilities.py TPI_F_0.txt

   O resultado será impresso no terminal e gravado no arquivo:
   sol_TPI_F_0.txt

4. Execução de todas as instâncias:
   ./run_all.sh TPI_F_0.txt TPI_F_1.txt TPI_F_2.txt

5. Exemplos de resultados obtidos:
   - TPI_F_0.txt  → Objetivo = 165.000000
                    Facilidades abertas: [1, 2]
                    Atribuições: (1,2), (1,3), (2,1)

6. Observações:
   - Caso queira exportar o modelo em formato LP legível:
     python3.10 solve_facilities.py TPI_F_0.txt --print-model

   - Arquivos de saída são gerados automaticamente com prefixo "sol_".
   - Todos os testes foram executados no Ubuntu (via WSL).

------------------------------------------------------------
FIM DO ARQUIVO
------------------------------------------------------------

