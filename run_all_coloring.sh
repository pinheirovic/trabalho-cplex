#!/bin/bash

echo "Rodando todas as instâncias de coloração..."

for f in TPI_COL_*.txt; do
    echo "===================================="
    echo "Rodando $f"
    python3.10 solve_coloring.py "$f"
done

echo "Concluído."
