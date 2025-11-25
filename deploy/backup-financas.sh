#!/bin/bash

# Script de backup automático do banco de dados
# Mantém os últimos 7 backups

BACKUP_DIR=~/backups/financas
DATE=$(date +%Y%m%d_%H%M%S)

# Criar diretório de backup se não existir
mkdir -p $BACKUP_DIR

# Fazer backup do banco de dados
cp ~/apps/planilha-financeira/instance/financas.db $BACKUP_DIR/financas_$DATE.db

# Manter apenas os últimos 7 backups
cd $BACKUP_DIR
ls -t | tail -n +8 | xargs -r rm

echo "Backup realizado: financas_$DATE.db"
