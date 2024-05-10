# PayApp Django Project Setup Guide


1. Install requirements:

```
pip install -r requirements.txt
```

2. Apply database migrations:

```
python manage.py makemigrations
python manage.py migrate
```

3. Run development server with self-cert HTTPS:

```
python manage.py runserver_plus --cert localhost.pem
```

Bypass any security warnings given by the browser.

## Troubleshooting
If the certificate files don't work, delete them and create new ones:
```
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout localhost.key -out localhost.crt
cat localhost.crt localhost.key > localhost.pem
```

If there is no admin user, create a superuser with:
```
python manage.py createsuperuser
```

To run without SSL:
```
python manage.py runserver
```