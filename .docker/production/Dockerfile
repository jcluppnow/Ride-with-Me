FROM ubuntu:focal

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
    libpq-dev postgresql-client
    #apt-get clean all & rm -rf /var/apt/lists* && rm -rf /var/cache/apt*

# Install Node/NPM
RUN curl -sL https://deb.nodesource.com/setup_16.x | bash - && \
    apt-get install -y -qq nodejs

RUN echo '#!/bin/bash\npython3.8 manage.py "$@"' > /usr/bin/dj && \
    chmod +x /usr/bin/dj

# Copy project and env file
COPY ./src /var/www/ride_with_me
COPY .env /var/www/ride_with_me/.env.readonly

# Python dependencies
WORKDIR /var/www/ride_with_me/application
RUN pip install --no-cache-dir --user -r requirements.txt

# Install node modules and build
RUN npm install --only=prod
RUN npm run prod

WORKDIR /var/www/ride_with_me

RUN mkdir /var/www/uploads
RUN ln -s /var/www/uploads /var/www/ride_with_me/uploads

# boot sh should run migrations and start django server
COPY .docker/production-boot.sh /boot.sh
RUN chmod +x /boot.sh
ENTRYPOINT ["/boot.sh"]
