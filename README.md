Никиян Тигран К0609-23

# CRUD приложение на Flask + PostgreSQL + Nginx + Redis

## Запуск и примеры запросов

```bash
docker-compose up --build


curl -X POST http://localhost/users -H "Content-Type: application/json" -d '{"name": "Vladimir", "email": "admin@example.com"}'

curl http://localhost/users

curl http://localhost/users/1

curl -X PUT http://localhost/users/1 -H "Content-Type: application/json" -d '{"email": "new@example.com"}'

curl -X DELETE http://localhost/users/1

curl -I http://localhost/users

docker compose logs -f nginx   
docker compose logs -f db      
docker compose logs -f web      