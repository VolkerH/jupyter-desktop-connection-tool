#!/bin/bash
# find first available port, we don't want to use the standard 8888 jupyter port
FREEPORT=`/usr/bin/python3 -c 'import socket; s=socket.socket(); s.bind(("", 0)); print(s.getsockname()[1]); s.close()'`
echo $FREEPORT > $HOME/.jupyter_docker_port
docker run --rm  \
          --gpus all \
          -p 10.11.19.188:$FREEPORT:8888 \
          -v $HOME:/home/jovyan/readonly_$USER \
          -v /shared/$USER:/home/jovyan/shared_$USER \
          spacem/jupyter-desktop-server 2> $HOME/.jupyter_docker_stderr
echo http://10.11.19.177:$FREEPORT/

# Below is an attempt to change the user ID but it causese errrors sarting up the
# containter ....
#export myUID=$(id -u)
#export myGID=$(id -g)
# https://medium.com/faun/set-current-host-user-for-docker-container-4e521cef9ffc
#docker run --rm  \
#          --user $myUID:$myGID \
#          --privileged \
#          --volume="/etc/group:/etc/group:ro" \
#          --volume="/etc/passwd:/etc/passwd:ro" \
#          --volume="/etc/shadow:/etc/shadow:ro" \
#          --gpus all \
#          -p 10.11.19.188:$FREEPORT:8888 \
#          -v $HOME:/localhome \
#          -v /tmp/dockershare:/dockershare \
#          spacem/jupyter-desktop-server 2> .jupyter_docker_stderr
