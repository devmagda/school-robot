#!/bin/bash
docker ps -a -q
docker volume ls -q

docker rm -f $(docker ps -a -q)
docker volume rm $(docker volume ls -q)

rm -rf postgres_data