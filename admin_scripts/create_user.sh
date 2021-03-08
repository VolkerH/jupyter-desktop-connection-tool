#!/bin/bash
# create the user (this will bring up an interactive shell)
echo "====================================="
echo "Creating new user $1"
echo "please add name and credentials below"
echo "====================================="
echo
adduser $1
echo
echo "====================================="
echo "Adding  $1 to docker group"
echo "====================================="
usermod -aG docker $1
echo
echo "====================================="
echo "Creating shared directory in /shared/$1"
echo "====================================="
mkdir -p /shared/$1
echo "Changing ownnership and permissions in /shared/$1"
chown -R $1 /shared/$1 
chmod a+rwx /shared/$1

echo
echo
echo "====================================="
echo "Generating key pair for remote access and adding"
echo "to ~$1/.ssh/authorized_keys"
echo "====================================="
ssh-keygen -f key_$1 -q -N ""
USERHOME=/home/$1
mkdir -p $USERHOME/.ssh && chown -R $1 $USERHOME/.ssh
chmod 700 $USERHOME/.ssh
cat key_$1.pub >> $USERHOME/.ssh/authorized_keys
chmod 644 $USERHOME/.ssh/authorized_keys


echo
echo "====================================="
echo "User generated"
echo "provide file key_$1 to user for access !"