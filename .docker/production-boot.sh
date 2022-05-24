#!/bin/bash

cd /var/www/ride_with_me
dj collectstatic --noinput
dj migrate
echo "Booting gunicorn..."
python3.8 -m gunicorn --bind 0.0.0.0:8000 --workers=3 ride_with_me.wsgi --log-file /var/log/ride_with_me/gunicorn.log --log-level critical --capture-output --access-logfile /var/log/ride_with_me/access.log &
echo "Booting daphne..."
python3.8 -m daphne -b 0.0.0.0 -p 8001 ride_with_me.asgi:application --access-log=/var/log/ride_with_me/daphne-access.log
