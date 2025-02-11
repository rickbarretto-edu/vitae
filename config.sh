#!/usr/bin/env bash

set -e  # Para encerrar em caso de erro

# Obtém o diretório do script e define o caminho absoluto do projeto
PROJECT_ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

# Adiciona o diretório src ao PYTHONPATH
export PYTHONPATH="$PROJECT_ROOT/src:$PYTHONPATH"

# Exibe o novo PYTHONPATH
echo "PYTHONPATH atualizado: $PYTHONPATH"