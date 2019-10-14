# API Integration

Коллекция сценариев для работы с различными API.

## Установка
### Docker Compose
```bash
# Клонировать репозиторий на локальную машину
git clone https://github.com/Ragnaruk/api_integration.git

# Перейти в папку репозитория
cd api_integration

# Запустить файл установки с командой prepare
make prepare

# Скопировать учетные данные пользователя Google в файл ./credentials/credentials.json
# Скопировать учетные данные пользователя Zulip в файл ./credentials/zuliprc.txt
# Изменить файл ./config/config.py
# Изменить файл ./docker-compose.yaml

# Собрать Docker образ
docker-compose build

# Запустить Docker контейнеры
docker-compose up -d

# Перейти по ссылкам из консоли для авторизации в Google
```
### Вне Docker
```bash
# Клонировать репозиторий на локальную машину
git clone https://github.com/Ragnaruk/api_integration.git

# Перейти в папку репозитория
cd api_integration

# Запустить файл установки с командой prepare
make prepare

# Скопировать учетные данные пользователя Google в файл /credentials/credentials.json
# Скопировать учетные данные пользователя Zulip в файл /credentials/zuliprc.txt
# Изменить файл /config/config.py

# Запустить файл установки с командой install
make install

# Запустить желаемый сценарий
python ./scenarios/...

# Перейти по ссылкам из консоли для авторизации в Google
```

## Обновление
```bash
# Запустить файл установки с командой update
make update
```