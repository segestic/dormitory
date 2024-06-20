#!/bin/bash

pip3 install -r requirements.txt
python3.10 manage.py collectstatic 
python3.10 manage.py makemigrations
python3.10 manage.py migrate
python3.10 manage.py migrate accounts

