# Usar a imagem oficial do Python 3.12
FROM python:3.12-slim

# Definir a variável de ambiente para evitar a interação durante a instalação de pacotes
ENV PYTHONUNBUFFERED 1

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo requirements.txt para o diretório de trabalho
COPY requirements.txt /app/

# Instalar dependências do sistema e pacotes necessários
RUN apt-get update && apt-get install -y \
    tzdata \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libpango-1.0-0 \
    libglib2.0-0 \
    shared-mime-info \
    libpangoft2-1.0-0 \
    libgl1-mesa-glx \
    gcc \
    libmariadb-dev \
    libmariadb-dev-compat \
    pkg-config \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    && ln -fs /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*  # Limpeza extra após a instalação

# Instalar as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o restante dos arquivos do projeto para o diretório de trabalho
COPY . /app/

# Definir variáveis de ambiente para Django
ENV PYTHONPATH /app

# Realizar as migrações do banco de dados no build
RUN python manage.py migrate --noinput

# Expor a porta em que o Django estará rodando
EXPOSE 8001

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8001"]
