#!/bin/bash
/etc/init.d/mysql start &&
IP=`hostname -i`
echo "10.67.130.53 app11utv-sth" >> /etc/hosts
echo "192.168.0.1 psw.test" >> /etc/hosts
/passwordstate/.venv/bin/python /passwordstate/app/manage.py makemigrations api
/passwordstate/.venv/bin/python /passwordstate/app/manage.py migrate
/passwordstate/.venv/bin/python /passwordstate/app/manage.py runserver "$IP":8000