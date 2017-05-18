FROM python:3.5
MAINTAINER Kislenko Maksim <m.kislenko@corp.mail.ru>

# COPY ./deploy/nova_sources.txt /etc/apt/sources.list
# RUN apt-get update && apt-get install nginx

# COPY ./deploy/nginx.conf /etc/nginx/sites-available/central.conf

# WORKDIR /etc/nginx/sites-enabled
# RUN ln -s ../sites-available/central.conf ./central.conf && rm -f default

WORKDIR /opt/central
COPY . .
# RUN chmod 777 ./start.sh
RUN pip3 install -r requirements.txt

EXPOSE 80
CMD ["python", "manage.py", "runserver", "80"]