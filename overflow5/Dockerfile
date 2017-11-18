####
#
# overflow5 CTF challenge Dockerfile
#
# Erik Hunstad - 06 NOV 17
#
# Build cmd
#   docker build -t overflow5 .
# Run cmd (must enable ptrace for gdb)
#   docker run -it --rm --cap-add=SYS_PTRACE overflow5
#
####

# Use ubuntu base (for glibc etc)
FROM ioft/i386-ubuntu:16.04
ENV CHALLENGE overflow5

# Update and set up environment
RUN apt-get update --fix-missing && apt-get -y upgrade && \
    apt-get install -y build-essential gdb nano netcat openssh-client \
                       python-minimal vim && \
    apt-get clean && \
    useradd -u 1000 -s /bin/bash flag && \
    useradd -u 1001 -s /bin/bash -m user

# Copy in our challenge files
WORKDIR /home/user/
COPY challenge_files/ ./

# Compile the challenge and set up permissions
RUN gcc -fno-stack-protector -fno-pic -z execstack -o ${CHALLENGE} ${CHALLENGE}.c && \
    chown user:user * && \
    chown flag:flag flag ${CHALLENGE} && \
    chmod 400 flag && \
    chmod 4755 ${CHALLENGE} && \
    chmod a+x pattern checksec.sh

# Set the default command to bash
USER user
CMD ["/bin/bash"]
