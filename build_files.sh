#!/bin/bash

pip3 install -r requirements.txt
python3.9 manage.py collectstatic 
python3.9 manage.py makemigrations
python3.9 manage.py migrate
python3.9 manage.py migrate accounts

