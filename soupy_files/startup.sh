#!/bin/bash

docker build -t soupy_files .
docker run -p 8200:80 --name soupy_files -d soupy_files
