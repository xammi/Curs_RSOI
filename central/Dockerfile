FROM python:3.5
MAINTAINER Kislenko Maksim <m.kislenko@corp.mail.ru>

WORKDIR /opt/central
COPY . .

RUN pip3 install -r requirements.txt
CMD ["python3", "manage.py", "runserver", "37001"]