FROM python:latest
COPY . /app
WORKDIR /app
RUN pip3 install django pillow
CMD python manage.py runserver 0.0.0.0:1111