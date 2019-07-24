web: cd ecommerce && gunicorn ecommerce.wsgi
release: python ecommerce/manage.py makemigrations --merge
release: python ecommerce/manage.py migrate
