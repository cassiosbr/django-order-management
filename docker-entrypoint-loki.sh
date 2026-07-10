#!/bin/bash
set -e

# Criar diretórios necessários
mkdir -p /loki/boltdb-shipper-active
mkdir -p /loki/boltdb-cache
mkdir -p /loki/chunks

# Executar Loki
exec loki "$@"
