FROM jfloff/alpine-python:2.7-slim

# Initialize the image
RUN adduser -D -u 1000 -s /bin/bash user && \
    addgroup user user && \
    ./entrypoint.sh -p colorama

# Set up challenge files
WORKDIR /home/user/
COPY cyber_haiku.py log.py ./
RUN chown user:user ./*

# Set up environment
USER user
EXPOSE 5000

CMD ["./cyber_haiku.py"]
