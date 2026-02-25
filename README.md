# Развертывание проекта

---
1. Клонирование проекта - ```git clone https://github.com/iMWC-IXIVI/EffectiveMobile.git```
2. Создание виртуального окружения, находясь в папке с проектом - ```python -m venv venv ```
3. Активация виртуального окружения - ```venv\Scripts\activate```
4. Создание .env файла (необходимо настроить) - ```copy .env_example .env```
5. Установка зависимостей - ```pip install -r req.txt```
6. Создание Docker образа - ```docker build -f Dockerfile -t eff_mobile_test .```
7. Запуск Docker образа - ```docker run -p 8000:8000 --env-file .env eff_mobile_test```
> Порт начинается с флага -p, левый порт (до двоеточий) какой порт будет на локальной машине-сервере, 
> правый, тот который указан внутри файла .env в переменной окружения DOCKERFILE_PORT.
> Если DOCKERFILE_PORT=8001 и вам нужно запустить образ на локальной машине на порту 98674, то команда будет следующая
> ```docker run -p 98674:8001 --env-file .env eff_mobile_test```
