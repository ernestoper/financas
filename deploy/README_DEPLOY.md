# 🚀 Deploy Simplificado - Raspberry Pi 5 com Tunnel Existente

Guia rápido para adicionar a aplicação financeira ao seu Cloudflare Tunnel existente em `mangueia.com`.

## ✅ Informações do Setup

- **Domínio**: mangueia.com
- **Tunnel existente**: eye-tracking-poc.mangueia.com (porta 5000)
- **Nova aplicação**: financas.mangueia.com (porta **5001**)
- **Plataforma**: Raspberry Pi 5

> ⚠️ **Nota**: Esta aplicação usa a porta **5001** para evitar conflito com sua aplicação Flask existente na porta 5000.

## 📦 1. Preparar a Aplicação na Raspberry Pi

```bash
# Conectar via SSH na Raspberry Pi
ssh pi@seu-ip-raspberry

# Criar diretório para a aplicação
mkdir -p ~/apps
cd ~/apps

# Clonar o repositório
git clone <seu-repositorio> planilha-financeira
cd planilha-financeira

# Configurar variáveis de ambiente
cp .env.example .env
nano .env
```

Configure o `.env`:
```bash
# Gerar SECRET_KEY segura
python3 -c "import secrets; print(secrets.token_hex(32))"

# Adicionar ao .env
SECRET_KEY=<cole-a-chave-gerada-aqui>
FLASK_ENV=production
```

## 🌐 2. Adicionar Rota ao Tunnel Existente

```bash
# Editar configuração do tunnel
nano ~/.cloudflared/config.yml
```

Adicione a nova rota (escolha o subdomínio que preferir):
```yaml
tunnel: SEU_TUNNEL_ID
credentials-file: /home/pi/.cloudflared/SEU_TUNNEL_ID.json

ingress:
  # Aplicação existente
  - hostname: eye-tracking-poc.mangueia.com
    service: http://localhost:5000
  
  # ADICIONE esta linha para a aplicação financeira
  - hostname: financas.mangueia.com
    service: http://localhost:5001
  
  # Rota padrão (sempre a última)
  - service: http_status:404
```

```bash
# Configurar DNS no Cloudflare
cloudflared tunnel route dns SEU_TUNNEL_NAME financas.mangueia.com

# Reiniciar o tunnel
sudo systemctl restart cloudflared
```

## 🔄 3. Configurar Auto-Start da Aplicação

```bash
# Criar serviço systemd
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

```bash
# Habilitar e iniciar o serviço
sudo systemctl daemon-reload
sudo systemctl enable financas-app.service
sudo systemctl start financas-app.service

# Verificar status
sudo systemctl status financas-app.service
```

## ✅ 4. Verificar Funcionamento

```bash
# Verificar container
docker ps | grep financeiro-app

# Verificar logs
cd ~/apps/planilha-financeira
docker-compose logs -f

# Testar localmente
curl http://localhost:5001

# Acessar via internet
# https://financas.mangueia.com
```

## 🔧 5. Comandos Úteis

### Gerenciar Aplicação
```bash
# Ver status
sudo systemctl status financas-app.service

# Reiniciar
sudo systemctl restart financas-app.service

# Parar
sudo systemctl stop financas-app.service

# Ver logs
cd ~/apps/planilha-financeira
docker-compose logs -f
```

### Atualizar Aplicação
```bash
cd ~/apps/planilha-financeira
sudo systemctl stop financas-app.service
git pull
docker-compose up -d --build
sudo systemctl start financas-app.service
```

### Gerenciar Tunnel
```bash
# Ver status
sudo systemctl status cloudflared

# Reiniciar
sudo systemctl restart cloudflared

# Ver logs
sudo journalctl -u cloudflared -f
```

## 💾 6. Backup Automático (Opcional)

```bash
# Copiar script de backup
cp deploy/backup-financas.sh ~/
chmod +x ~/backup-financas.sh

# Testar backup
~/backup-financas.sh

# Agendar backup diário às 3h da manhã
crontab -e
```

Adicione:
```
0 3 * * * /home/pi/backup-financas.sh >> /home/pi/backup-financas.log 2>&1
```

## 🎯 Checklist Final

- [ ] Aplicação clonada em `~/apps/planilha-financeira`
- [ ] `.env` configurado com SECRET_KEY
- [ ] Rota adicionada ao `~/.cloudflared/config.yml` (porta **5001**)
- [ ] DNS configurado: `financas.mangueia.com`
- [ ] Tunnel reiniciado: `sudo systemctl restart cloudflared`
- [ ] Serviço systemd criado e habilitado
- [ ] Container rodando: `docker ps`
- [ ] Site acessível: `https://financas.mangueia.com`
- [ ] Auto-start funcionando após reboot
- [ ] Backup configurado (opcional)

## 🐛 Troubleshooting

### Porta 5001 já em uso
```bash
# Verificar o que está usando a porta
sudo netstat -tulpn | grep 5001

# Ou escolher outra porta (5002, 5003, etc)
# Edite: run.py, docker-compose.yml, Dockerfile e config.yml do tunnel
```

### Aplicação não inicia
```bash
docker-compose logs
sudo systemctl status financas-app.service
```

### Erro 502 Bad Gateway
```bash
# Verificar se container está rodando
docker ps

# Verificar se porta está correta no tunnel
cat ~/.cloudflared/config.yml

# Testar localmente
curl http://localhost:5001
```

### Tunnel não conecta
```bash
# Ver logs do tunnel
sudo journalctl -u cloudflared -n 50

# Verificar configuração
cat ~/.cloudflared/config.yml

# Reiniciar tunnel
sudo systemctl restart cloudflared
```

## 📊 Monitoramento

```bash
# Recursos da Raspberry Pi
htop
vcgencmd measure_temp
df -h

# Logs em tempo real
docker-compose logs -f
sudo journalctl -u cloudflared -f
sudo journalctl -u financas-app -f
```

## 🔐 Segurança

- ✅ SSL/HTTPS automático via Cloudflare Tunnel
- ✅ Porta 5001 não exposta publicamente (apenas localhost)
- ✅ SECRET_KEY única e segura no `.env`
- ✅ Firewall pode bloquear porta 5001 (acesso apenas via tunnel)

## 📝 Resumo da Configuração

| Item | Valor |
|------|-------|
| **Domínio** | mangueia.com |
| **Subdomínio** | financas.mangueia.com |
| **Porta Local** | 5001 |
| **Container** | financeiro-app |
| **Diretório** | ~/apps/planilha-financeira |
| **Serviço** | financas-app.service |
| **Auto-start** | ✅ Sim (systemd) |
| **SSL** | ✅ Sim (Cloudflare) |

---

**Última atualização**: Novembro 2025  
**Testado em**: Raspberry Pi 5 com Raspberry Pi OS (64-bit)
