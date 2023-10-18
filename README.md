# Создаем контейнеры
` docker compose up `

# Добавляем вопросы в бд
```
curl --location 'localhost:8000/quiz/random' \
--header 'Content-Type: application/json' \
--data '{
    "question_num": 1
}'
```

# Ищем вопрос по айди
```
curl --location 'localhost:8000/question/get?question_id=1'
```
