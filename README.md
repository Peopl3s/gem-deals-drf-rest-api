# Gem Deals RestAPI

## Установка/Запуск
```bash
git clone https://github.com/Peopl3s/gem-deals-drf-rest-api.git

cd .\gem-deals-drf-rest-api\

docker compose up
```
## Использование 
API URL - http://127.0.0.1/api/v1 (принимает POST и GET-запросы).

GET-запрос - Выдача обработанных данных: В ответе содержится поле "response" со списком из 5 клиентов, потративших наибольшую сумму за весь период.
```bash
curl -GET http://127.0.0.1/api/v1/
```

POST-запрос - Загрузка файла для обработки: Принимает из POST-запроса .csv файл, обрабатывает и сохраняет извлеченные из файла данные в БД проекта.
```bash
curl -i -X POST -H "Content-Type: multipart/form-data" -F "deals=@<путь_до_файла>" http://127.0.0.1/api/v1/
```

## Ключевые особенности
* Кэширование данных, возвращаемых GET-эндпоинтом, реализовано на основе Redis
* Настройки проекта разделены на local и production (БД для local - SQLite, для prod - PostgreSQL)
  ```bash
  python manage.py runserver --settings=gem_deals.settings.local
  python manage.py runserver --settings=gem_deals.settings.prod
  ```
* Nginx отвечает за обработку входящих запросов на 80 порт и переадресацию их в uWSGI.
* PostgreSQL, Nginx, Redis и DRF-приложение находятся в отдельных контейнерах и управляются через docker compose
* Код покрыт тестами (Django Test suite)
  ```bash
  python manage.py test --settings=gem_deals.settings.local
  ```
* При обработке файлов применяется DI, что в дальнейшем облегчит добавление поддержки других форматов файлов
* Обеспечена атомарность транзакций
  


