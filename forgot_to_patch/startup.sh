#!/bin/bash

# Build Mysql server
docker run -p 3306:3306 --name "wordpress-mysql" -e MYSQL_ROOT_PASSWORD='aSHITTYpassword123!@#' -e MYSQL_DATABASE=wordpress -e MYSQL_USER=wordpress -e MYSQL_PASSWORD='ANOTHERshittyPASSWORD#@!123' -d mysql

#Build Web Server
docker build -t forgot_to_patch .
docker run -p 5001:80 --name forgot_to_patch --link wordpress-mysql -d forgot_to_patch
