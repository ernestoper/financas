#!/bin/bash

echo "🚀 Iniciando Sistema de Controle Financeiro..."

# Verificar se o Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 não encontrado. Instale o Python 3 primeiro."
    exit 1
fi

# Criar ambiente virtual se não existir
if [ ! -d "venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv venv
fi

# Ativar ambiente virtual
echo "🔧 Ativando ambiente virtual..."
source venv/bin/activate

# Instalar dependências
echo "📥 Instalando dependências..."
pip install -q -r requirements.txt

# Popular dados se for primeira vez
if [ ! -f "financas.db" ]; then
    echo "📊 Populando banco de dados com seus dados..."
    python popular_dados.py
else
    # Migrar banco existente
    echo "🔄 Verificando se precisa migrar banco de dados..."
    python migrar_banco.py
fi

# Rodar aplicação
echo "✅ Tudo pronto! Iniciando servidor..."
echo ""
echo "🌐 Acesse: http://localhost:5000"
echo "👤 Usuários: ernesto/senha123 ou antonietta/senha123"
echo ""
python app.py
