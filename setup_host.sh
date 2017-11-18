#!/bin/bash

#
# Perform initial host setup for a challenge server.
#

# Disable dmesg output for normal users
sudo sysctl -w kernel.dmesg_restrict=1
echo 'kernel.dmesg_restrict=1' | sudo tee -a /etc/sysctl.conf

# Disable ASLR for overflow challenges
sudo sysctl -w kernel.randomize_va_space=0
echo 'kernel.randomize_va_space=0' | sudo tee -a /etc/sysctl.conf
