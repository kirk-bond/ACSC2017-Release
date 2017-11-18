#!/bin/bash

docker build -t otp .
docker run -p 24000:24000 --name otp -d otp
