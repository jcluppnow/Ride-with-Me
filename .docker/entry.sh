#!/bin/bash

chown django:django -R /home/django/src
su django --command "/usr/local/bin/boot.sh"
