#!/bin/bash
export PATH=$PATH:/Users/gabep/Scripts/
source ~/Virtualenvs/dalme/bin/activate
source /Users/gabep/Repos/DALME-Online-Database/env
cd /Users/gabep/Repos/DALME-Online-Database
docker compose -f docker-compose.eb.yml run dalme.web python manage.py collectstatic --noinput
docker compose -f docker-compose.eb.yml run dalme.web python manage.py compress --verbosity=0
