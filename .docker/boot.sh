#!/bin/bash

TESTING=0
if [[ $ENV == "testing" ]]; then
  echo "Using testing env"
  TESTING=1
  cp /tmp/django/.env.testing ./.env.readonly
else
  echo "Using local env"
  cp /tmp/django/.env ./.env.readonly
fi

cd application
npm install
npm run watch-poll &
cd ..
if [[ $TESTING == 1 ]]; then
  echo "Removing sqlite DB"
  rm *sqlite*
else
  echo "Migrating DB"
  dj migrate
fi
dj runserver 0.0.0.0:4444
