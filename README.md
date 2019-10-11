# ApiIntegration

Коллекция скриптов для работы с различными API.

## Установка
```bash
# Скопировать репозиторий на локальную машину
git pull https://github.com/Ragnaruk/ApiIntegration

# Перейти в директорию с репозиторием
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