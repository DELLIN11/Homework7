#!/bin/bash
# Запускаем Gunicorn в фоновом режиме, слушаем unix-сокет
gunicorn --bind unix:/run/app.sock --workers 4 app:app &

# Запускаем Nginx на переднем плане, чтобы контейнер не умирал
nginx -g "daemon off;"