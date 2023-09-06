# Foodgram
##### Сервис обмена рецептами любимых блюд.
###
##### Адрес сервиса: https://foodgramweb.hopto.org
#
## Стек:

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray) 	![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)



#### Запуск проекта:
Клонируйте репозиторий и подготовьте сервер:
```
docker-compose.production.yml <username>@<host>:/home/<username>/foodgram/
nginx.conf <username>@<host>:/home/<username>/foodgram/
.env <username>@<host>:/home/<username>/foodgram/
```

Установите docker и docker-compose:
```
sudo apt install docker.io 
sudo apt install docker-compose
```

Соберите контейнеры и выполните миграции:
```
sudo docker compose -f docker-compose.production.yml up -d
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
          
```

Соберите статику и создайте суперюзера:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
sudo docker exec -it foodgram-backend-1 bash (в зависимости от наименования контейнера backend на вашем сервере)
python manage.py createsuperuser
```
Импортируйте ингредиенты:
```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py importdata
```
