FROM node:22

# Instalar Chrome
RUN apt-get update && apt-get install -y \
    chromium \
    && rm -rf /var/lib/apt/lists/*

# Configurar aplicação
WORKDIR /app
COPY . .
RUN npm install

# Usar Chromium do sistema
ENV PUPPETEER_SKIP_CHROMIUM_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium

# Criar diretório para tokens
RUN mkdir -p /app/tokens && chmod -R 777 /app/tokens

# Iniciar aplicação
CMD ["node", "index.js"]