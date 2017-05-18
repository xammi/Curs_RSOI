FROM python:3.5
MAINTAINER Kislenko Maksim <m.kislenko@corp.mail.ru>

WORKDIR /opt/central
COPY . .
RUN pip3 install -r requirements.txt

EXPOSE 80
CMD ["python", "manage.py", "runserver", "0.0.0.0:80"]