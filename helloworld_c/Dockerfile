####
#
# helloworld_c CTF challenge Dockerfile
#
# Erik Hunstad - 19 APR 17
#
# Build cmd
#   docker build -t helloworld_c .
# Run cmd
#   docker run -it --rm --network=none helloworld_c
#
####

# Use a small python docker
FROM alpine

# Update and set up environment
RUN apk add --update --no-cache bash vim nano && \
    adduser -D -u 1000 -s /bin/bash flag && \
    adduser -D -u 1001 -s /bin/bash user

# Copy in our challenge files
WORKDIR /home/user/
COPY challenge_files/ ./

# Set up permissions
RUN chown user:user * && \
    chown flag:flag flag hello_world suid_c_wrapper && \
    chmod 400 flag && \
    chmod 500 hello_world && \
    chmod 4755 suid_c_wrapper

# Set the default command to bash
USER user
CMD ["/bin/bash"]
