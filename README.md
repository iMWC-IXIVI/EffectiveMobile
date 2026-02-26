# EffectiveMobile Task

---
## Стэк
> FastAPI
> PyJWT
> Alembic
> PostgreSQL
> Docker
> SQLAlchemy
> Uvicorn
> Pydantic + pydantic-settings

## Развертывание проекта
1. Клонирование проекта - ```git clone https://github.com/iMWC-IXIVI/EffectiveMobile.git```
2. Создание виртуального окружения, находясь в папке с проектом (Windows) - ```python -m venv venv```
3. Создание виртуального окружения, находясь в папке с проектом (Linux) - ```python3 -m venv vevn```
4. Активация виртуального окружения (Windows) - ```venv\Scripts\activate```
5. Активация виртуального окружения (Linux) - ```source venv/bin/activate```
6. Создание .env файла (необходимо настроить) (Windows) - ```copy .env_example .env```
7. Создание .env файла (необходимо настроить) (Linux) - ```cp .env_example .env```
8. Установка зависимостей (Windows) - ```pip install -r req.txt```
9. Установка зависимостей (Linux) - ```pip3 install -r req.txt```
10. Создание Docker образа - ```docker build -f Dockerfile -t eff_mobile_test .```
11. Запуск Docker образа - ```docker run -p 8000:8000 --env-file .env eff_mobile_test```
> Порт начинается с флага -p, левый порт (до двоеточий) какой порт будет на локальной машине-сервере, 
> правый, тот который указан внутри файла .env в переменной окружения DOCKERFILE_PORT.
> Если DOCKERFILE_PORT=8001 и вам нужно запустить образ на локальной машине на порту 98674, то команда будет следующая
> ```docker run -p 98674:8001 --env-file .env eff_mobile_test```
12. Запуск docker-compose - ```docker compose up --build```
13. Просмотр файлов системы контейнера - ```docker exec -it fastapi_backend bash```
14. Создание миграции (Контейнер должен быть запущен) - ```docker exec -it fastapi_backend alembic revision --autogenerate -m "Название миграции"```
> После создания миграции необходимо перезагрузить контейнер, что бы миграции накатились

---
## Паттерны
> 1. Swagger - GET /docs
> 2. Регистрация пользователя - POST /user/registration
> 3. Вход пользователя - POST /user/login
> 4. Обновление access токена - POST /user/refresh
> 5. Выход из системы - POST /user/logout
> 6. Детальная информация о пользователе - GET /user/detail
> 7. Удаление пользователя - DELETE /user/delete
> 8. Изменение профиля - PATCH /user/detail/update

--- 

## Система разграничения прав доступа

```text
В системе присутствуют 2 типа прав, 1 - manager это простые пользователи, становятся при регистрации,
2 - admin, это пользователи, имеющий полный доступ к системе, они могут получать список всех пользователей
и назначать администраторов.
```
