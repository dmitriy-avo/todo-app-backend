FROM node:20-alpine

WORKDIR /app

# Копируем package.json и lock-файл — кэшируем установку зависимостей
COPY package.json package-lock.json ./
RUN npm install

# Копируем остальной код
COPY . .

EXPOSE 3000

# Запуск dev-сервера
CMD ["npm", "start"]
