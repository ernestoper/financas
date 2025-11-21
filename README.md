# 💰 Sistema de Controle Financeiro Familiar

Sistema web completo para controle financeiro familiar com múltiplos usuários.
Tudo em um único servidor Flask - simples e funcional!

## 🚀 Tecnologias

- **Backend:** Flask (Python)
- **Frontend:** HTML + Tailwind CSS + JavaScript
- **Banco de Dados:** SQLite
- **Autenticação:** Session-based

## 📋 Funcionalidades

- ✅ Login para você e sua esposa
- ✅ Dashboard com visão geral das finanças
- ✅ **Dados reais já cadastrados** (R$ 8.500 receitas, R$ 6.737 despesas)
- ✅ **Controle mensal** - cada mês tem suas próprias despesas
- ✅ **Copiar mês anterior** - duplica despesas com 1 clique
- ✅ **Editar despesas** - ajuste valores mês a mês
- ✅ Controle de receitas e despesas fixas
- ✅ Acompanhamento da reserva de emergência (meta: R$ 40.500)
- ✅ Registro de gastos variáveis do dia a dia
- ✅ Marcar despesas como "pagas"
- ✅ Seletor de mês/ano no dashboard e despesas
- ✅ Histórico completo
- ✅ Responsivo (funciona no celular)

## 🛠️ Instalação e Uso

### Opção 1: Script Automático (Linux/Mac) - RECOMENDADO
```bash
./iniciar.sh
```
Este script vai:
- Criar ambiente virtual
- Instalar dependências
- Popular o banco com seus dados reais
- Iniciar o servidor

### Opção 2: Manual
```bash
# Criar ambiente virtual
python3 -m venv venv

# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Popular banco de dados com seus dados
python popular_dados.py

# Rodar o sistema
python app.py
```

## 🌐 Acesso

1. Abra o navegador
2. Acesse: **http://localhost:5000**
3. Login:
   - **Usuário:** ernesto | **Senha:** senha123
   - **Usuário:** antonietta | **Senha:** senha123

## 👥 Usuários

- **Ernesto:** ernesto / senha123
- **Antonietta:** antonietta / senha123

(Altere as senhas após primeiro login)

## 📱 Como Usar

1. Faça login
2. **Seus dados já estão cadastrados!** (receitas e despesas fixas)
3. Registre gastos do dia a dia conforme acontecem
4. Marque despesas como "pagas" quando quitar
5. Registre depósitos na reserva de emergência
6. Acompanhe seu progresso no dashboard

## 🔒 Segurança

- Senhas criptografadas
- Autenticação JWT
- Dados isolados por família
