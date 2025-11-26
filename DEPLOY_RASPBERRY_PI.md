# 🚀 Deploy na Raspberry Pi 5 (Setup Existente)

Guia para adicionar a aplicação financeira ao seu ambiente Raspberry Pi 5 já configurado com Cloudflare Tunnel.

## ✅ Informações do Ambiente

- **Domínio**: `mangueia.com`
- **Tunnel ID**: `27f3f4da-f61a-4e9a-bdbf-44eb21c6c087`
- **Tunnel Existente**: `eye-tracking.mangueia.com` (porta 5000)
- **Nova Aplicação**: `financas.mangueia.com` (porta **5001**)
- **Container**: `financeiro-app`

---

## 📦 1. Instalação da Aplicação

```bash
# 1. Conectar na Raspberry Pi
ssh ernesto@192.168.192.81

# 2. Criar diretório e clonar
mkdir -p ~/apps
cd ~/apps
git clone <seu-repo> 
cd financas

# 3. Configurar ambiente
cp .env.example .env

# Gerar uma nova SECRET_KEY segura (copie o resultado)
python3 -c 'import secrets; print(secrets.token_hex(16))'

# Editar o arquivo .env
nano .env
# 1. Procure a linha SECRET_KEY=...
# 2. Apague o valor padrão e cole sua chave gerada
# 3. Salve: Ctrl+O, Enter, Ctrl+X
```

## 🌐 2. Criar Subdomínio DNS

Primeiro, vamos criar o subdomínio no Cloudflare. Escolha **UMA** das opções:

### Opção A: Automática (Recomendado) ⚡

Na Raspberry Pi, rode:

```bash
cloudflared tunnel route dns 27f3f4da-f61a-4e9a-bdbf-44eb21c6c087 financas.mangueia.com
```

Este comando cria automaticamente o registro DNS CNAME no Cloudflare.

### Opção B: Manual (Painel Cloudflare) 🖱️

1. Acesse [dash.cloudflare.com](https://dash.cloudflare.com)
2. Selecione o domínio **mangueia.com**
3. Vá em **DNS** → **Records**
4. Clique em **Add record**:
   - **Type**: `CNAME`
   - **Name**: `financas`
   - **Target**: `27f3f4da-f61a-4e9a-bdbf-44eb21c6c087.cfargotunnel.com`
   - **Proxy status**: ✅ Proxied (laranja)
5. **Save**

---

## ⚙️ 3. Configurar Cloudflare Tunnel

Você **NÃO** precisa criar um novo tunnel. Vamos apenas adicionar uma rota ao existente.

### 3.1. Configurar Credenciais (Importante!) 🔑

O serviço do sistema precisa acessar o arquivo de credenciais. Vamos movê-lo para a pasta correta:

```bash
# 1. Copiar arquivo de credenciais (ajuste o nome do arquivo .json se necessário)
sudo cp ~/.cloudflared/27f3f4da-f61a-4e9a-bdbf-44eb21c6c087.json /etc/cloudflared/cert.json

# 2. Ajustar permissões de segurança
sudo chown root:root /etc/cloudflared/cert.json
sudo chmod 600 /etc/cloudflared/cert.json
```

### 3.2. Editar Configuração do Tunnel

```bash
# Editar configuração do tunnel
sudo nano /etc/cloudflared/config.yml
```

Adicione a nova rota para a aplicação financeira (porta 5001):

```yaml
tunnel: 27f3f4da-f61a-4e9a-bdbf-44eb21c6c087
credentials-file: /etc/cloudflared/cert.json

ingress:
  # Aplicação existente (NÃO ALTERAR)
  - hostname: eye-tracking.mangueia.com
    service: http://localhost:5000
  
  # NOVA ROTA - Aplicação Financeira (ADICIONAR)
  - hostname: financas.mangueia.com
    service: http://localhost:5001
  
  # Rota padrão (sempre a última)
  - service: http_status:404
```

Salve o arquivo (`Ctrl+O`, `Enter`, `Ctrl+X`).

**Reiniciar o Tunnel:**

```bash
sudo systemctl restart cloudflared

# Verifique se reiniciou com sucesso
sudo systemctl status cloudflared
```

> **✅ Pronto!** O tunnel agora serve dois subdomínios:
> - `eye-tracking.mangueia.com` → porta 5000
> - `financas.mangueia.com` → porta 5001

## 🐳 4. Iniciar Aplicação

```bash
cd ~/apps/planilha-financeira

# Construir a imagem (importante na primeira vez ou após atualizações)
docker compose build

# Iniciar container
docker compose up -d

# Verificar se está rodando na porta 5001
docker ps | grep financeiro-app
```

## 🔄 5. Configurar Auto-Start

Para garantir que a aplicação inicie automaticamente se a Raspberry Pi reiniciar:

```bash
# Criar serviço
sudo nano /etc/systemd/system/financas-app.service
```

Cole o conteúdo:

```ini
[Unit]
Description=Aplicação Financeira Familiar
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ernesto/apps/planilha-financeira
ExecStart=/usr/bin/docker compose up -d
ExecStop=/usr/bin/docker compose down
User=ernesto

[Install]
WantedBy=multi-user.target
```

Habilitar o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable financas-app.service
sudo systemctl start financas-app.service
```

## ✅ 6. Verificação Final

1. Acesse `https://financas.mangueia.com` no navegador.
2. Se a Raspberry Pi reiniciar:
   - O Docker inicia.
   - O serviço `financas-app` sobe o container na porta 5001.
   - O serviço do tunnel conecta e expõe o subdomínio.

Tudo automático! 🚀