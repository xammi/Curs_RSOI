FROM python:3.5
MAINTAINER Kislenko Maksim <m.kislenko@corp.mail.ru>

WORKDIR /opt/oauth
COPY . .
RUN pip3 install -r requirements.txt
RUN python manage.py migrate

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]