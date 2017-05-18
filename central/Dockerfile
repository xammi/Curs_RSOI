FROM python:3.5
MAINTAINER Kislenko Maksim <m.kislenko@corp.mail.ru>

RUN apt-get update && apt-get install nginx

WORKDIR /etc/nginx/sites-available
COPY ./deploy/nginx.conf ./central.conf

WORKDIR /etc/nginx/sites-enabled
RUN ln -s ../sites-available/vitrine.conf ./vitrine.conf \
    && rm -f default

WORKDIR /opt/central
COPY . .
RUN chmod 777 ./start.sh
EXPOSE 80

RUN pip3 install -r requirements.txt
CMD ["./start.sh"]