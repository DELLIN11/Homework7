FROM python:3.11-slim

# Устанавливаем nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Подкидываем конфиг Nginx и даем права скрипту
COPY nginx.conf /etc/nginx/nginx.conf
RUN chmod +x start.sh

# Запускаем наш скрипт
CMD ["./start.sh"]