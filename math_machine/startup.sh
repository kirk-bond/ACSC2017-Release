#!/bin/bash

docker build -t math_machine .
docker run -p 5000:5000 --name math_machine -d math_machine
