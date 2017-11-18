#!/bin/bash
###
#
# Docker ssh CTF challenge setup script for Ubuntu
#
# Erik Hunstad - 14 APR 16
#
###

# User vars
CHALLENGE_NAME="overflow3"
PASSWORD="overflow"
SSH_BANNER_TEXT="Overflow 3 - Call on me by Eric Prydz"

SHELL_NAME=$CHALLENGE_NAME
SHELL_NAME+="_shell"
# Must be root to run the script

if [ ! $UID = "0" ]; then
    echo "[ERROR] You must be root to run this script"
    exit 1
fi

# Are we cleaning up?

if [ "$1" = "-c" ]; then
    # Remove the challenge user
    userdel -r $CHALLENGE_NAME
    # Remove the challenge shell entry
    sed -i /$CHALLENGE_NAME/d /etc/shells
    # Remove the challnege shell file
    rm /usr/local/bin/$HELL_NAME
    # Remove the custom ssh banner
    sed -i /$CHALLENGE_NAME/d /etc/ssh/sshd_config
    # Remove the docker image
    docker rm $CHALLENGE_NAME
    # Remove any dangling images (left over from the challenge image build)
    docker rmi $(docker images -f dangling=true -q)
    exit 0
fi


echo "[!] This will install docker, and add a user ($CHALLENGE_NAME) to your system."
read -p  "[?] Press [Enter] to continue or [Ctrl+C] to quit."

# Check for and install docker

echo "[?] Checking for docker..."
docker -v >/dev/null 2>&1 || { 
    echo >&2 "[!] No docker found. Installing now"
    apt-get update
    apt-get install \
        apt-transport-https \
        ca-certificates \
        curl \
        software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    add-apt-repository \
        "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
         $(lsb_release -cs) \
        stable"
    apt-get update
    apt-get install docker-ce
}

# Build the challenge docker

echo '[+] Building the challenge docker'
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR  && docker build -t $CHALLENGE_NAME .

# Add a user for the challenge 

echo '[+] Adding a user for the challenge'
useradd -m -g docker $CHALLENGE_NAME
echo "$CHALLENGE_NAME:$PASSWORD" | chpasswd
touch /home/$CHALLENGE_NAME/.hushlogin
echo -e "\n$SSH_BANNER_TEXT\n" > /home/$CHALLENGE_NAME/banner.txt

# Create a new "shell" for the challenge user

echo '[+] Creating a new "shell" for the challenge user'
touch /usr/local/bin/$SHELL_NAME
chmod +x /usr/local/bin/$SHELL_NAME
echo "/usr/local/bin/$SHELL_NAME" >> /etc/shells
chsh -s /usr/local/bin/$SHELL_NAME $CHALLENGE_NAME

# Create the "shell" that spawns a new docker image

echo '[+] Making the shell spawn a new challenge docker each run'
echo -e "#!/bin/bash\ndocker run -it --rm --network=none --user=user -w /home/user --privileged $CHALLENGE_NAME" > /usr/local/bin/$SHELL_NAME

# Clean up ssh logins for challenge users

echo '[+] Setting the ssh banner for the challenge user'
echo -e "Match User $CHALLENGE_NAME\n\tBanner /home/$CHALLENGE_NAME/banner.txt" >> /etc/ssh/sshd_config
service ssh restart

# Done!

echo '[!] Finished. Give out the following information:'
echo -e "\tUsername: $CHALLENGE_NAME"
echo -e "\tPassword: $PASSWORD"

