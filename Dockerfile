# Multi-stage build para otimizar tamanho da imagem

# Stage 1: Builder
FROM python:3.11-slim as builder

# Instalar dependências de sistema necessárias para build
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

# Criar usuário não-root para segurança
RUN useradd -m -u 1000 appuser

# Criar diretório de trabalho
WORKDIR /app

# Copiar dependências Python do builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código da aplicação
COPY --chown=appuser:appuser . .

# Criar diretório para o banco de dados
RUN mkdir -p /app/instance && \
    chown -R appuser:appuser /app/instance

# Mudar para usuário não-root
USER appuser

# Adicionar .local/bin ao PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Expor porta
EXPOSE 5001

# Variáveis de ambiente
ENV FLASK_APP=run.py
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5001').read()" || exit 1

# Comando para iniciar a aplicação
CMD ["python", "run.py"]
