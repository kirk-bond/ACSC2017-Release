FROM ubuntu:16.04

# Initialize the image
RUN useradd -u 1000 -s /bin/bash -m user && \
    apt-get update && \
    apt-get -y install python-minimal python-pip && \
    pip2 install --upgrade pip && \
    pip2 install colorama pyinotify && \
    apt-get clean

# Set up challenge files
WORKDIR /home/user/
COPY temp_files.py log.py flag ./
RUN chmod 555 temp_files.py log.py && \
    chmod 444 flag

# Set up environment
USER user
EXPOSE 5000

CMD ["./temp_files.py"]
