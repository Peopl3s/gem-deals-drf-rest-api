![image](https://github.com/Peopl3s/gem-deals-drf-rest-api/assets/28685107/0c9c2616-4697-4d45-8fc2-b14229b5b3ff)# Gem Deals RestAPI <img style="height:55px; width:55px;" src="https://opengameart.org/sites/default/files/styles/medium/public/gems_preview.png" alt="gems"/>

## Установка/Запуск
```bash
git clone https://github.com/Peopl3s/gem-deals-drf-rest-api.git

cd .\gem-deals-drf-rest-api\

docker compose up
```
## Использование 
API URL - http://127.0.0.1/api/v1/    (принимает POST и GET-запросы).

GET-запрос - Выдача обработанных данных: В ответе содержится поле "response" со списком из 5 клиентов, потративших наибольшую сумму за весь период.
```bash
curl -GET http://127.0.0.1/api/v1/
```

POST-запрос - Загрузка файла для обработки: Принимает из POST-запроса .csv файл, обрабатывает и сохраняет извлеченные из файла данные в БД проекта.
```bash
curl -i -X POST -H "Content-Type: multipart/form-data" -F "deals=@<путь_до_файла>" http://127.0.0.1/api/v1/
```

### Через Postman

<details>
  <summary>👆</summary>
<img style="height:380px; width:1000px;" src="https://i.ibb.co/C9x68CX/post.png" alt="post"/>
<img style="height:380px; width:1000px;" src="https://i.ibb.co/2F7zGjV/get.png" alt="get"/>
</details>

## Ключевые особенности
* Кэширование данных, возвращаемых GET-эндпоинтом, реализовано на основе [Redis](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/gem_deals/gem_deals/settings/prod.py#L26)
* Настройки проекта [разделены](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/gem_deals/gem_deals/settings/prod.py#L1) на local и production (БД для local - SQLite, для prod - PostgreSQL)
  ```bash
  python manage.py runserver --settings=gem_deals.settings.local
  python manage.py runserver --settings=gem_deals.settings.prod
  ```
* [Nginx](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/config/nginx/default.conf.template#L1) отвечает за обработку входящих запросов на 80 порт и их переадресацию в uWSGI.
* PostgreSQL, Nginx, Redis и DRF-приложение находятся в отдельных контейнерах и управляются через [docker compose](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/docker-compose.yml#L1)
* Код покрыт [тестами](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/gem_deals/deal_api/tests/test_services.py#L1) (Django Test suite)
  ```bash
  python manage.py test --settings=gem_deals.settings.local
  ```
* При обработке файлов [применяется DI](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/gem_deals/deal_api/services.py#L15), что в дальнейшем облегчит добавление возможности обрабатывать файлы других форматов
* Обеспечена [атомарность транзакций](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/gem_deals/deal_api/services.py#L134)
* Настроено [логирование](https://github.com/Peopl3s/gem-deals-drf-rest-api/blob/661864a8cbe49f7672d703d3872df88ed7c91474/gem_deals/gem_deals/settings/base.py#L134C1-L134C1) в файл
* Код документирован, code style Black, используются аннотации типов.

<hr>
<details>
  <summary>env-файлы в репозитории</summary>
  <i>.env-файлы обычно не принято хранить в публичном репозитории (как правило использую заглушку по типу .env.example), но для удобства сдачи работы было принято решение оcтавить всё-таки их в репозитории.</i>
</details>
  


