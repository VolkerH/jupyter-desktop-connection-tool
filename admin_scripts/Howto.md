# Create a new user

On the server/workstation, run the `create_user.sh` script in this folder as sudo.

This will create the user, add them to the docker group and generate a
private/public key. The public key file is addes to the new user's `.ssh/authorized_hosts`. The private key file is written to the working directory and needs to be provided with the connection tool for authentication.

