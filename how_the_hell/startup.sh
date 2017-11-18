#!/bin/bash

docker build -t how_the_hell .
docker run -p 8181:80 --name how_the_hell -d how_the_hell
