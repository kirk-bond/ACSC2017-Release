####
#
# SQL foo  CTF challenge Dockerfile
#
# Jake Harding - 15 AUG 17
# template by Erik Hunstad - 13 APR 17
#
# Build cmd
#   docker build -t sql_foo .
# Run cmd
#   docker run -it --rm --network=none sql_foo
#
####


# Use a small python docker
FROM jfloff/alpine-python:2.7

# Add a non root user
RUN apk add --update --no-cache vim nano && \
    adduser -D -u 1000 -s /bin/bash flag && \
    adduser -D -u 1001 -s /bin/bash user

# Copy in our challenge files
WORKDIR /home/user/
COPY challenge_files/ ./

# Build and set up permissions - Users should not have access to sql.py and
# names.txt. suid_python_wrapper should be setuid and everything else RO.
RUN gcc -o suid_python_wrapper suid_python_wrapper.c && \
    chmod 770 /home/flag && \
    chown user:user * && \
    chown flag:flag sql.py names.txt suid_python_wrapper && \
    chmod 500 sql.py && \
    chmod 400 names.txt && \
    chmod 4755 suid_python_wrapper && \
    chmod 444 flag suid_python_wrapper.c wordlist

# Set the default command to bash
USER user
CMD ["/bin/bash"]
