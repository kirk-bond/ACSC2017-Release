####
#
# helloworld_py CTF challenge Dockerfile
#
# Erik Hunstad - 13 APR 17
#
# Build cmd
#   docker build -t helloworld-py .
# Run cmd
#   docker run -it --rm --network=none helloworld-py
#
####

# Use a small python docker
FROM jfloff/alpine-python:2.7-slim

# Update and set up environment - colorama is needed for log.py
RUN apk add --update --no-cache bash vim nano && \
    adduser -D -u 1000 -s /bin/bash flag && \
    adduser -D -u 1001 -s /bin/bash user && \
    ./entrypoint.sh -p colorama

# Copy in our challenge files
WORKDIR /home/user/
COPY challenge_files/ ./

# Set up permissions - intentionally make log.py writable by competitors due to
# a bad group assignment (vuln)
RUN chown user:user * && \
    chown flag:flag flag hello_world.py suid_python_wrapper && \
    chown flag:user log.py && \
    chmod 400 flag && \
    chmod 774 hello_world.py log.py && \
    chmod 4755 suid_python_wrapper

# Set the default command to bash
USER user
CMD ["/bin/bash"]
