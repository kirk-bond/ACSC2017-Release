####
#
# math_machine CTF challenge Dockerfile
#
# Build - Troy Ward - 1 NOV 17
####

FROM jfloff/alpine-python:2.7-slim

# Initialize the image
RUN adduser -D -u 1000 -s /bin/bash user && \
    addgroup user user && \
    ./entrypoint.sh

# Set up challenge files
WORKDIR /home/user/
COPY math_machine.py ./
RUN chown user:user ./*

# Set up the environment
USER user
EXPOSE 5000

CMD ["./math_machine.py"]
