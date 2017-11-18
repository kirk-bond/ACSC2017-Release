####
#
# ssh-host CTF challenges Dockerfile
#
# Erik Hunstad - 11 NOV 17
#
# Build cmd
#   docker build -t ssh-host .
#   docker build -t overflow1 ../overflow1/
#   docker build -t overflow2 ../overflow2/
#   docker build -t overflow3 ../overflow3/
#   docker build -t overflow4 ../overflow4/
#   docker build -t overflow5 ../overflow5/
#
# Run cmd
#   docker run -v /var/run/docker.sock:/var/run/docker.sock ssh-host
#
# NOTE: The build process has been automated with docker-compose. Run
#   `docker-compose build` to build all containers and dependencies automatically.
#
# NOTE: The host of this container will have to disable dmesg and ASLR. See
#   `setup_host.sh` for info
#
# Please ignore how sloppy it is to repeat each command 5 times instead of looping
####

# Use ubuntu base (because thats what setup_ubuntu.sh expects ;)
FROM ubuntu:16.04

MAINTAINER Erik Hunstad <yourdockerfilebroke@threecone.com>

# Update and set up environment (clean and rm to keep image size down)
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get install --no-install-recommends -y \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common \
    openssh-server \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Add Docker repo key
RUN curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -

# Add Docker repo
RUN add-apt-repository -y \
    "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) \
    stable"

# Install Docker
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && \
    apt-get install --no-install-recommends -y docker-ce \
    && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set up individual challenges
COPY setup.sh ./
RUN ./setup.sh helloworld-c helloworld \
        "\nhelloworld-c\n" \
        "docker run -it --rm --network=none helloworld-c"
RUN ./setup.sh helloworld-c2 helloworld \
        "\nhelloworld-c2\n" \
        "docker run -it --rm --network=none helloworld-c2"
RUN ./setup.sh helloworld-py helloworld \
        "\nhelloworld-py\n" \
        "docker run -it --rm --network=none helloworld-py"
RUN ./setup.sh overflow1 overflow \
        "\nOverflow 1 - Nice and easy\n" \
        "docker run -it --rm --network=none --cap-add=SYS_PTRACE overflow1"
RUN ./setup.sh overflow2 overflow \
        "\nOverflow 2 - It's all about control\n" \
        "docker run -it --rm --network=none --cap-add=SYS_PTRACE overflow2"
RUN ./setup.sh overflow3 overflow \
        "\nOverflow 3 - Call on me by Eric Prydz\n" \
        "docker run -it --rm --network=none --cap-add=SYS_PTRACE overflow3"
RUN ./setup.sh overflow4 overflow \
        "\nOverflow 4 - no calls, now what?\n" \
        "docker run -it --rm --network=none --cap-add=SYS_PTRACE overflow4"
RUN ./setup.sh overflow5 overflow \
        "\nOverflow 5 - checksec, pattern, and gdb included\n" \
        "docker run -it --rm --network=none --cap-add=SYS_PTRACE overflow5"
RUN ./setup.sh sql-foo sql \
        "\nSQL Foo - Python\n" \
        "docker run -it --rm --network=none sql"

# No fork bombs!
#RUN echo "overflow1 hard nproc 50" >> /etc/security/limits.conf \
#    && echo "overflow2 hard nproc 50" >> /etc/security/limits.conf \
#    && echo "overflow3 hard nproc 50" >> /etc/security/limits.conf \
#    && echo "overflow4 hard nproc 50" >> /etc/security/limits.conf \
#    && echo "overflow5 hard nproc 50" >> /etc/security/limits.conf

# Expose port 22 (remap with docker on the host i.e. -p 2222:22)
EXPOSE 22

# SSH requries this
RUN mkdir -p /var/run/sshd

# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

# By default, just run `ssh -D`
CMD ["/usr/sbin/sshd", "-D"]
