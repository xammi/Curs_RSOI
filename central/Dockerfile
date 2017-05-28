FROM python:3.5
MAINTAINER Kislenko Maksim <m.kislenko@corp.mail.ru>

# копирование файлов проекта в контейнер
WORKDIR /opt/central
COPY . .

# установка зависимостей
RUN pip3 install -r requirements.txt

# создание базы данных
RUN python manage.py migrate

# запуск серверного приложения на 80-ом порту контейнера
EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]