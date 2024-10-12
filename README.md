# MAINlaptop

Перед запуском проекта убедитесь, что у вас установлена обученная модель best.pt 

### Запуск проекта в контейнере Docker

1. Скопировать переменные окружения для tg-bot

```
cp bot/.env.example bot/.env
cp bot/.env.example .env
```

2. Скопировать обученную модель в директории с кодом

```
cp best.pt bot/best.pt 
cp best.pt flask/best.pt 
```

2. Собрать образы контейнеров 

```
docker-compose build
```

3. Запустить проект

```
docker-compose up -d
```