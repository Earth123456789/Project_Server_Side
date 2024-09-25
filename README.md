# Project 

```sh
py -m venv myvenv

myvenv\Scripts\activate.bat

pip install django

pip install psycopg2 cryptography PyJWT requests django-allauth pillow

```

then 

Retore backup.sql in Pgadmin

then 

```sh

python manage.py migrate

python manage.py runserver

```
