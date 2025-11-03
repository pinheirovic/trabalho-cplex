#!/bin/bash

# Criar pasta para salvar logs, se não existir
mkdir -p resultados

# Ativar venv se estiver usando
source venv/bin/activate

# Loop apenas pelos arquivos de instância
for f in TPI_F_*.txt; do
    echo "===================="
    echo "Rodando $f"
    python3.10 solve_facilities.py "$f" | tee "resultados/resultado_$f.txt"
done
