#!/bin/bash -e

#
# Setup script for a new docker ssh shell container. Invoke this script
# when building the master docker ssh-host in order to set up individual
# sub-containers for challenges.
#
# Usage: ./setup.sh <username> <password> <banner> <shell-command>
#

if [[ $# -ne 4 ]]; then
    echo "Usage: ./setup.sh <username> <password> <banner> <shell-command>"
    exit 1
fi

username=$1
password=$2
banner=$3
shell_command=$4

# Add the user
useradd -m -g docker ${username}
echo "${username}:${password}" | chpasswd

# Hush login and add ssh banner
touch /home/${username}/.hushlogin
echo -e "${banner}" > /home/${username}/banner.txt
echo -e "Match User ${username}\n\tBanner /home/${username}/banner.txt" >> /etc/ssh/sshd_config

# Set the login shell
echo -e "#!/bin/bash\n${shell_command}" > /usr/local/bin/${username}
chmod a+x /usr/local/bin/${username}
echo "/usr/local/bin/${username}" >> /etc/shells
chsh -s /usr/local/bin/${username} ${username}
