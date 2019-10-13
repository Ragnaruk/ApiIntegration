# API Integration

Коллекция скриптов для работы с различными API.

## Установка
```bash
# Клонировать репозиторий на локальную машину
git clone https://github.com/Ragnaruk/ApiIntegration.git

# Перейти в папку репозитория
cd ApiIntegration

# Запустить файл установки
make prepare

# Скопировать учетные данные пользователя Google в файл /credentials/credentials.json
# Скопировать учетные данные пользователя Zulip в файл /credentials/zuliprc.txt
# Изменить файл /config/config.py

# Собрать Docker образ
docker-compose build

# Запустить Docker контейнер
docker-compose up -d
```
