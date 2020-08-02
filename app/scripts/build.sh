#!/bin/bash

docker-compose up -d --build # Build all images from docker-compose
sleep 10                     # Sleep to let services start ex postgres, before making migrations
docker-compose run --rm backend alembic upgrade head
docker-compose run --rm backend python3 app/db/data_init.py
