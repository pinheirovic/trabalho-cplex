#!/bin/bash

# ===============================
# Script para preparar o ambiente e rodar todas as instâncias
# ===============================

# Pastas
RESULT_DIR="resultados"
SOL_DIR="soluções"

mkdir -p $RESULT_DIR
mkdir -p $SOL_DIR

# Criar e ativar venv se não existir
if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual venv..."
    python3.10 -m venv venv
fi

source venv/bin/activate

# Instalar docplex se ainda não estiver instalado
pip show docplex > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Instalando docplex..."
    pip install docplex
fi

# Configurar PYTHONPATH para o CPLEX
export PYTHONPATH=/opt/ibm/ILOG/CPLEX_Studio2211/cplex/python/3.10/x86-64_linux:$PYTHONPATH

# Rodar todas as instâncias TPI_F_*.txt
for f in TPI_F_*.txt; do
    echo "===================="
    echo "Rodando $f"
    python3.10 solve_facilities.py "$f" | tee "$RESULT_DIR/resultado_$f.txt"
    # Mover arquivos de saída para soluções/
    mv sol_$f $SOL_DIR/
done

echo "===================="
echo "Execução completa! Logs em $RESULT_DIR/, soluções em $SOL_DIR/"
