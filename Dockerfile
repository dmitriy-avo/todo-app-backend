# Базовый образ Python
FROM python:3.12-slim

# Рабочая директория внутри контейнера
WORKDIR /app

# Сначала копируем только requirements — чтобы Docker кэшировал слой с зависимостями
# (если requirements не менялся, pip install не будет повторяться при каждой сборке)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Теперь копируем весь код приложения
COPY . .

# Порт, на котором работает uvicorn
EXPOSE 8000

# Команда запуска
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
