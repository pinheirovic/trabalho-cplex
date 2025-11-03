Trabalho - Uso do CPLEX via Python
==================================

Autor: Victor Albino
Ambiente: Linux (Ubuntu via WSL)
Solver: IBM ILOG CPLEX Optimization Studio 22.1.1
Linguagem: Python 3.10

---

INSTRUÇÕES DE CONFIGURAÇÃO
--------------------------

1. Certifique-se de que o CPLEX esteja instalado no Linux:
   /opt/ibm/ILOG/CPLEX_Studio2211/

2. Ative o Python 3.10 (ou superior) e instale as dependências:
sudo python3.10 -m pip install docplex

3. Copie todos os arquivos do projeto para uma pasta, por exemplo:
~/trabalho-cplex

---

INSTRUÇÕES DE EXECUÇÃO
----------------------

1. Para executar uma única instância:
python3.10 solve_facilities.py TPI_F_0.txt

O resultado será salvo em um arquivo `sol_TPI_F_0.txt`.

2. Para executar todas as instâncias automaticamente:
bash run_all.sh

Os resultados serão gravados em:
- `sol_TPI_F_0.txt`
- `sol_TPI_F_1.txt`
- `sol_TPI_F_2.txt`

---

ESTRUTURA DO PROJETO
--------------------

├── solve_facilities.py # Script principal que chama o CPLEX
├── run_all.sh # Executa todas as instâncias
├── TPI_F_0.txt # Instância 1
├── TPI_F_1.txt # Instância 2
├── TPI_F_2.txt # Instância 3
├── .gitignore
└── README.txt # Este arquivo

---

INFORMAÇÕES ADICIONAIS
----------------------

- O script `solve_facilities.py` lê o arquivo de instância `.txt` e resolve o problema de localização de facilidades.
- As soluções são salvas automaticamente em arquivos `.txt` com prefixo `sol_`.
- Testado no Ubuntu 24.04 com CPLEX 22.1.1 e Python 3.10.
