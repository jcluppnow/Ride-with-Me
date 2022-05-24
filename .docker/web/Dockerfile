FROM ubuntu:focal

ARG ENV
ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive
ENV LANG C.UTF-8

RUN apt-get update -qq && apt-get install -y -qq \
    git less nano curl \
    ca-certificates \
    wget build-essential unzip \
    # Python
    python3.8 python3.8-dev python3.8-venv python3-pip gettext \
    # GeoDjango Dependencies
    gdal-bin binutils libproj-dev libgdal-dev \
    # PostgreSQL Connection
    libpq-dev postgresql-client \
    # Spatialite Dependencies
    libspatialite-dev libsqlite3-mod-spatialite
    #apt-get clean all & rm -rf /var/apt/lists* && rm -rf /var/cache/apt*

# Install Node/NPM
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y -qq nodejs

RUN echo '#!/bin/bash\npython3.8 manage.py "$@"' > /usr/bin/dj && \
    chmod +x /usr/bin/dj


# Install ngrok
WORKDIR /tmp

RUN wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip && \
    unzip ngrok-stable-linux-amd64.zip

RUN mv ngrok /usr/local/bin


# might not need this
EXPOSE 4444

# Python dependencies
COPY ./src/application/requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /tmp/django
COPY .env .env.testing /tmp/django/

RUN useradd -G www-data,root -u 1001 -d /home/django django

RUN mkdir -p /home/django/src && chown django:django -R /home/django
WORKDIR /home/django/src

# boot sh should run migrations and start django server
COPY .docker/entry.sh /entry.sh
RUN chmod +x /entry.sh

COPY .docker/boot.sh /usr/local/bin/boot.sh
RUN chmod +x /usr/local/bin/boot.sh

CMD ["/entry.sh"]
