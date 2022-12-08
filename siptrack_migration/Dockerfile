FROM ubuntu:14.04
ENV DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8\
    LANGUAGE=en_US:en\
    PYTHONIOENCODING=utf-8

COPY . /passwordstate/app/

RUN mkdir -p /passwordstate/.venv &&\
    apt-get update &&\
    apt-get install -y python2.7 \
                    python-pip \
                    python-dev \
                    python-virtualenv\
                    mysql-server \
                    mysql-client \
                    libmysqlclient-dev \
                    vim

RUN /etc/init.d/mysql start &&\
    sleep 2 &&\
    mysql -e "create database passwordstate;" &&\
    mysql -e "CREATE USER 'ps_user'@'localhost' IDENTIFIED BY 'passwordstate';" &&\
    mysql -e "GRANT ALL PRIVILEGES ON passwordstate.* TO 'ps_user'@'localhost';" &&\
    /etc/init.d/mysql stop

RUN virtualenv --python python2 /passwordstate/.venv/ &&\
    cd /passwordstate/app/siptrack_fetch/siptrack/ &&\
    /passwordstate/.venv/bin/python setup.py install &&\
    /passwordstate/.venv/bin/pip install -r /passwordstate/app/requirement.txt &&\
    /etc/init.d/mysql start &&\
    sleep 2 &&\
    /passwordstate/.venv/bin/python /passwordstate/app/manage.py makemigrations &&\
    /passwordstate/.venv/bin/python /passwordstate/app/manage.py migrate &&\
    /etc/init.d/mysql stop



CMD "/passwordstate/app/startup.sh"