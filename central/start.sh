#!/bin/bash

service nginx start

python manage.py runserver 127.0.0.1:8080