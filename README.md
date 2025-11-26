# 💰 Controle Financeiro Familiar

Sistema completo de gestão financeira familiar com múltiplos usuários, metas de reserva personalizadas, recorrência automática e análises detalhadas em tempo real.

## ✨ Funcionalidades Principais

### 📊 Gestão Financeira
- **Receitas**: Registro de todas as fontes de renda (salários, freelances, investimentos)
- **Despesas Fixas**: Controle de contas recorrentes com vencimentos automáticos
- **Despesas Variáveis**: Acompanhamento de gastos do dia a dia por categoria
- **Recorrência Automática**: Despesas fixas são criadas automaticamente todo mês

### 🎯 Metas e Reservas
- **Múltiplas Metas de Reserva**: Crie metas personalizadas (Carro, Casa, Viagem, Emergência)
- **Acompanhamento Visual**: Gráficos de progresso para cada meta
- **Metas por Categoria**: Defina limites de gastos por categoria com alertas
- **Reserva de Emergência**: Controle dedicado para fundo de emergência

### 👥 Multi-usuário e Família
- **Sistema Multi-família**: Cada família tem seus próprios dados isolados
- **Gestão de Membros**: Adicione membros da família e controle permissões
- **Perfis Personalizados**: Avatar, configurações individuais e histórico
- **Painel Administrativo**: Gerenciamento completo de usuários e famílias

### 📈 Dashboard e Análises
- **Dashboard Interativo**: Visão geral completa das finanças
- **Gráficos Dinâmicos**: Visualização de receitas, despesas e tendências
- **Análise por Categoria**: Identifique onde seu dinheiro está sendo gasto
- **Histórico Mensal**: Acompanhe a evolução financeira ao longo do tempo

### 🎨 Interface Moderna
- **Design Responsivo**: Funciona perfeitamente em desktop, tablet e mobile
- **Notificações Toast**: Feedback visual para todas as ações
- **Tema Moderno**: Interface limpa e intuitiva
- **Ícones e Cores**: Personalize suas metas com ícones e cores

## 🛠️ Tecnologias Utilizadas

### Backend
- **Flask 3.0.0**: Framework web Python
- **SQLAlchemy 3.1.1**: ORM para banco de dados
- **SQLite**: Banco de dados leve e eficiente
- **Werkzeug 3.0.1**: Segurança e criptografia de senhas
- **Python-dotenv**: Gerenciamento de variáveis de ambiente

### Frontend
- **HTML5/CSS3**: Interface moderna e responsiva
- **JavaScript**: Interatividade e requisições AJAX
- **Chart.js**: Gráficos interativos
- **Font Awesome**: Ícones profissionais
- **Bootstrap**: Framework CSS para responsividade

### DevOps
- **Docker**: Containerização da aplicação
- **Docker Compose**: Orquestração de containers

## 📋 Requisitos

- Python 3.11 ou superior
- Docker e Docker Compose (para instalação via Docker)
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

## 🐳 Instalação com Docker (Recomendado)

```bash
# 1. Clone o repositório
git clone <seu-repo>
cd planilha-financeira

# 2. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env e defina uma SECRET_KEY segura

# 3. Inicie com Docker Compose
docker-compose up -d

# 4. Acesse a aplicação
# http://localhost:5001
```

## 💻 Instalação Manual

```bash
# 1. Clone o repositório
git clone <seu-repo>
cd planilha-financeira

# 2. Crie ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows

# 3. Instale dependências
pip install -r requirements.txt

# 4. Configure variáveis de ambiente
cp .env.example .env
# Edite o .env e defina uma SECRET_KEY segura

# 5. Execute a aplicação
python run.py

# 6. Acesse no navegador
# http://localhost:5001
```

## 🔧 Comandos Úteis

### Docker
```bash
# Iniciar aplicação
docker-compose up -d

# Ver logs em tempo real
docker-compose logs -f

# Parar aplicação
docker-compose down

# Rebuild após mudanças no código
docker-compose up -d --build

# Acessar shell do container
docker-compose exec web bash

# Reiniciar aplicação
docker-compose restart
```

### Administração
```bash
# Tornar um usuário administrador
python tornar_admin.py

# Verificar estrutura do banco de dados
python verificar_banco.py

# Popular dados de exemplo (desenvolvimento)
python popular_dados.py

# Verificar dados de família
python verify_family.py

# Verificar perfis de usuário
python verify_profile.py
```

### Desenvolvimento
```bash
# Ativar ambiente virtual
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Instalar novas dependências
pip install <pacote>
pip freeze > requirements.txt

# Executar em modo debug
export FLASK_ENV=development  # Linux/Mac
set FLASK_ENV=development     # Windows
python run.py
```

## 📁 Estrutura do Projeto

```
planilha-financeira/
├── app/
│   ├── __init__.py           # Inicialização do Flask
│   ├── extensions.py         # Extensões (SQLAlchemy)
│   ├── utils.py              # Funções utilitárias
│   ├── models/               # Modelos do banco de dados
│   │   ├── __init__.py
│   │   ├── core.py           # User, Familia, Profile
│   │   └── finance.py        # Receita, Despesa, Reserva, Metas
│   ├── routes/               # Rotas e controladores
│   │   ├── __init__.py
│   │   ├── auth.py           # Autenticação (login, registro)
│   │   ├── main.py           # Rotas principais (dashboard, páginas)
│   │   ├── api.py            # APIs REST (dados JSON)
│   │   └── admin.py          # Painel administrativo
│   └── services/             # Lógica de negócio
├── templates/                # Templates HTML
│   ├── base.html             # Template base
│   ├── login.html            # Página de login
│   ├── register.html         # Página de registro
│   ├── dashboard.html        # Dashboard principal
│   ├── receitas.html         # Gestão de receitas
│   ├── despesas_fixas.html   # Gestão de despesas fixas
│   ├── despesas_variaveis.html # Gestão de despesas variáveis
│   ├── reserva.html          # Gestão de reservas
│   ├── metas.html            # Metas por categoria
│   ├── perfil.html           # Perfil do usuário
│   ├── admin.html            # Painel admin
│   └── errors/               # Páginas de erro
│       ├── 404.html
│       └── 500.html
├── instance/                 # Banco de dados (não versionado)
│   └── financas.db
├── static/                   # Arquivos estáticos (CSS, JS, imagens)
├── venv/                     # Ambiente virtual Python
├── .env                      # Variáveis de ambiente (não versionado)
├── .env.example              # Exemplo de configuração
├── .gitignore                # Arquivos ignorados pelo Git
├── Dockerfile                # Configuração Docker
├── docker-compose.yml        # Orquestração Docker
├── requirements.txt          # Dependências Python
├── run.py                    # Ponto de entrada da aplicação
└── README.md                 # Este arquivo
```

## 🎯 Como Usar

### Primeiro Acesso
1. Acesse `http://localhost:5001`
2. Clique em "Registrar" para criar uma conta
3. Preencha os dados e crie sua família
4. Faça login com suas credenciais

### Configuração Inicial
1. Acesse o **Perfil** e personalize seu avatar
2. Configure suas **Receitas** mensais
3. Cadastre suas **Despesas Fixas** com recorrência
4. Crie suas **Metas de Reserva** personalizadas
5. Defina **Metas por Categoria** para controlar gastos

### Uso Diário
1. Registre **Despesas Variáveis** conforme gasta
2. Marque **Despesas Fixas** como pagas quando quitar
3. Adicione valores às suas **Reservas**
4. Acompanhe o **Dashboard** para visão geral

### Gestão Familiar
1. Convide membros da família (em desenvolvimento)
2. Cada membro pode registrar suas próprias despesas
3. Visualize gastos consolidados da família
4. Gerencie permissões e acessos

## 🔒 Segurança

- **Senhas Criptografadas**: Usando Werkzeug com hash bcrypt
- **Proteção CSRF**: Tokens de segurança em formulários
- **Sessões Seguras**: Cookies HTTP-only e secure
- **Validação de Dados**: Sanitização de inputs no backend
- **Isolamento de Dados**: Cada família acessa apenas seus próprios dados
- **Variáveis de Ambiente**: Credenciais sensíveis não versionadas

## 🔑 Variáveis de Ambiente

Crie um arquivo `.env` baseado no `.env.example`:

```bash
# Flask
SECRET_KEY=sua-chave-secreta-super-segura-aqui-mude-isso
FLASK_ENV=production

# Database (SQLite - não precisa configurar)
# DATABASE_URL=sqlite:///instance/financas.db
```

> ⚠️ **IMPORTANTE**: Sempre altere a `SECRET_KEY` em produção para uma chave aleatória e segura!

## 👨‍💼 Painel Administrativo

O sistema possui um painel administrativo completo para gerenciar usuários e famílias.

### Tornar Usuário Admin
```bash
python tornar_admin.py
```

### Funcionalidades Admin
- Visualizar todas as famílias cadastradas
- Gerenciar usuários do sistema
- Visualizar estatísticas globais
- Acessar logs e auditoria (em desenvolvimento)

## 🚀 Deploy em Produção

### Raspberry Pi 5 com Cloudflare Tunnel

Este é o método recomendado para deploy seguro com HTTPS automático e acesso via subdomínio.

#### Pré-requisitos
- Raspberry Pi 5 com Raspberry Pi OS (64-bit)
- Conta Cloudflare com domínio configurado
- Acesso SSH à Raspberry Pi

#### 1. Instalar Docker

```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Instalar Docker Compose
sudo apt install docker-compose -y

# Reiniciar
sudo reboot
```

#### 2. Preparar Aplicação

```bash
# Criar diretório
mkdir -p ~/apps
cd ~/apps

# Clonar repositório
git clone <seu-repo> planilha-financeira
cd planilha-financeira

# Configurar .env
cp .env.example .env
nano .env  # Configure SECRET_KEY

# Gerar SECRET_KEY segura
python3 -c "import secrets; print(secrets.token_hex(32))"
```

#### 3. Configurar Cloudflare Tunnel

```bash
# Instalar cloudflared
wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm64.deb
sudo dpkg -i cloudflared-linux-arm64.deb

# Autenticar
cloudflared tunnel login

# Criar tunnel
cloudflared tunnel create financas
# Anote o TUNNEL_ID exibido

# Criar configuração
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

Adicione no `config.yml`:
```yaml
tunnel: SEU_TUNNEL_ID
credentials-file: /home/pi/.cloudflared/SEU_TUNNEL_ID.json

ingress:
  - hostname: financas.seudominio.com
    service: http://localhost:5001
  - service: http_status:404
```

```bash
# Configurar DNS
cloudflared tunnel route dns financas financas.seudominio.com
```

#### 4. Configurar Auto-Start (Systemd)

**Serviço da Aplicação:**
```bash
sudo nano /etc/systemd/system/financas-app.service
```

Adicione:
```ini
[Unit]
Description=Aplicação Financeira Familiar
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/pi/apps/planilha-financeira
ExecStart=/usr/bin/docker-compose up -d
ExecStop=/usr/bin/docker-compose down
User=pi

[Install]
WantedBy=multi-user.target
```

**Serviço do Cloudflare Tunnel:**
```bash
sudo nano /etc/systemd/system/cloudflared-financas.service
```

Adicione:
```ini
[Unit]
Description=Cloudflare Tunnel - Financas
After=network.target

[Service]
Type=simple
User=pi
ExecStart=/usr/local/bin/cloudflared tunnel --config /home/pi/.cloudflared/config.yml run financas
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Habilitar serviços:**
```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Habilitar auto-start
sudo systemctl enable financas-app.service
sudo systemctl enable cloudflared-financas.service

# Iniciar agora
sudo systemctl start financas-app.service
sudo systemctl start cloudflared-financas.service

# Verificar status
sudo systemctl status financas-app.service
sudo systemctl status cloudflared-financas.service
```

#### 5. Verificar Funcionamento

```bash
# Verificar containers
docker ps

# Verificar logs
docker-compose logs -f
sudo journalctl -u cloudflared-financas.service -f

# Acessar aplicação
# https://financas.seudominio.com
```

#### 6. Backup Automático

```bash
# Criar script de backup
nano ~/backup-financas.sh
```

Adicione:
```bash
#!/bin/bash
BACKUP_DIR=~/backups/financas
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp ~/apps/planilha-financeira/instance/financas.db $BACKUP_DIR/financas_$DATE.db
cd $BACKUP_DIR
ls -t | tail -n +8 | xargs -r rm
echo "Backup realizado: financas_$DATE.db"
```

```bash
# Tornar executável
chmod +x ~/backup-financas.sh

# Agendar backup diário (3h da manhã)
crontab -e
# Adicione: 0 3 * * * /home/pi/backup-financas.sh >> /home/pi/backup-financas.log 2>&1
```

#### Comandos Úteis

```bash
# Gerenciar aplicação
sudo systemctl status financas-app.service
sudo systemctl restart financas-app.service
docker-compose logs -f

# Gerenciar tunnel
sudo systemctl status cloudflared-financas.service
sudo systemctl restart cloudflared-financas.service
sudo journalctl -u cloudflared-financas.service -f

# Atualizar aplicação
cd ~/apps/planilha-financeira
sudo systemctl stop financas-app.service
git pull
docker-compose up -d --build
sudo systemctl start financas-app.service

# Monitorar recursos
htop
vcgencmd measure_temp
df -h
```

### Outras Opções de Deploy

#### Servidor Linux Tradicional

```bash
# 1. Instale Docker e Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Clone e configure
git clone <seu-repo>
cd planilha-financeira
cp .env.example .env
nano .env  # Configure SECRET_KEY

# 3. Inicie
docker-compose up -d

# 4. Configure firewall (opcional)
sudo ufw allow 5001
```

### Considerações de Produção
- Use um servidor web reverso (Nginx/Apache)
- Configure SSL/HTTPS com Let's Encrypt
- Faça backup regular do banco de dados
- Monitore logs e performance
- Considere usar PostgreSQL para maior escala

## 🐛 Troubleshooting

### Aplicação não inicia
```bash
# Verifique logs
docker-compose logs -f

# Recrie containers
docker-compose down
docker-compose up -d --build
```

### Erro de banco de dados
```bash
# Verifique estrutura
python verificar_banco.py

# Recrie banco (CUIDADO: apaga dados)
rm instance/financas.db
python run.py
```

### Problemas de permissão
```bash
# Linux: ajuste permissões
sudo chown -R $USER:$USER .
chmod -R 755 .
```

## 📊 Roadmap

- [ ] Exportação de relatórios (PDF, Excel)
- [ ] Integração com bancos (Open Banking)
- [ ] App mobile (PWA)
- [ ] Notificações por email
- [ ] Gráficos de tendências e previsões
- [ ] Importação de extratos bancários
- [ ] API REST completa
- [ ] Modo escuro

## 📝 Licença

MIT License - Sinta-se livre para usar e modificar.

## 👥 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/MinhaFeature`)
3. Commit suas mudanças (`git commit -m 'Adiciona MinhaFeature'`)
4. Push para a branch (`git push origin feature/MinhaFeature`)
5. Abra um Pull Request

## 📧 Suporte

Para dúvidas e suporte:
- Abra uma [issue](link-para-issues)
- Consulte a documentação adicional na pasta do projeto

## 🙏 Agradecimentos

Desenvolvido com ❤️ para ajudar famílias a terem melhor controle financeiro.

---

**Versão**: 1.0.0  
**Última atualização**: Novembro 2025
