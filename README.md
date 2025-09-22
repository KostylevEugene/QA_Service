# QA_Service
QA_Service - это API-сервис для создания вопросов и ответов для них.


## Методы:
### Вопросы (Questions):
GET /questions/ — список всех вопросов  
POST /questions/ — создать новый вопрос  
GET /questions/{id} — получить вопрос и все ответы на него  
PATCH /questions/{id} - изменить текст вопроса  
DELETE /questions/{id} — удалить вопрос (вместе с ответами)


### Ответы (Answers):
POST /questions/{id}/answers/ — добавить ответ к вопросу  
GET /answers/{id} — получить конкретный ответ  
DELETE /answers/{id} — удалить ответ


## Запуск сервиса
1. Создать .env-файл на основе .env_template и заполните необходимые переменные.
2. Выполните команду docker compose up --build
3. Выполните команду docker compose exec qa_app alembic upgrade head или же войдите в контейнер самостоятельно с помощью docker compose exec qa_app sh и выполните команду alembic upgrade head.

## Тестирование сервиса
Для тестирования сервиса следует запустить файл test.sh 