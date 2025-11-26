#!/bin/bash
# Script de Backup Automático - Banco de Dados Finanças
# Copia o banco da Raspberry Pi para o PC local

DATA=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR=~/backups/financas

# Criar diretório se não existir
mkdir -p $BACKUP_DIR

# Fazer backup via SCP
echo "Iniciando backup do banco de dados..."
scp ernesto@192.168.192.81:~/apps/planilha-financeira/instance/financas.db \
    $BACKUP_DIR/financas_${DATA}.db

# Verificar sucesso
if [ $? -eq 0 ]; then
    echo "✅ Backup realizado com sucesso: financas_${DATA}.db"
    
    # Manter apenas últimos 30 backups
    cd $BACKUP_DIR
    COUNT=$(ls -1 financas_*.db 2>/dev/null | wc -l)
    if [ $COUNT -gt 30 ]; then
        echo "Removendo backups antigos..."
        ls -t financas_*.db | tail -n +31 | xargs -r rm
        echo "✅ Backups antigos removidos"
    fi
else
    echo "❌ Erro ao fazer backup!"
    exit 1
fi

echo "Total de backups: $(ls -1 $BACKUP_DIR/financas_*.db | wc -l)"
