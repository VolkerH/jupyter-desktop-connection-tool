import paramiko
import time
import re

HOSTIP = "10.11.19.188"
USER = "spacem"
PRIVATEKEYFILE = "/home/hilsenst/.ssh/id_rsa"

DOCKER_START_CMD = '$HOME/rundocker.sh'
DOCKER_STDERR_CMD =  "/usr/bin/cat $HOME/.jupyter_docker_stderr"
DOCKER_PORT_CMD = "/usr/bin/cat $HOME/.jupyter_docker_port"
DOCKER_KILL_CMD = "/usr/bin/killall docker"

SLEEPTIME = 5


def get_ssh_client_and_key(privatekeyfile=PRIVATEKEYFILE):
    k = paramiko.RSAKey.from_private_key_file(privatekeyfile)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return c,k

def connect(c, pkey, hostname=HOSTIP, user=USER):
    c.connect( hostname = hostname, username = user, pkey = pkey)


def start_server(c):
    stdin , stdout, stderr = c.exec_command(DOCKER_START_CMD)
    time.sleep(SLEEPTIME) # give server some time to start up

    # Jupyterlab sends connection URL to stderr, which
    # we redirect into a file in the startup script on 
    # the server. 
    stdin , stdout, stderr = c.exec_command(DOCKER_STDERR_CMD)
    catout = stdout.read()
    for line in catout.decode('utf-8').split("\n"):
        m = re.match(r'.*(?P<token>\?token=.+)', line)
        if m is not None:
            break
    token = m["token"]

    # The startup script on the server looks for an
    # available port number and redirects it into a file
    stdin , stdout, stderr = c.exec_command(DOCKER_PORT_CMD)
    port = stdout.read().decode('utf-8').strip()

    jupyterURL = f"http://{HOSTIP}:{port}/{token}"
    return jupyterURL

def kill_server(c):
    c.exec_command(DOCKER_KILL_CMD)

def disconnect(c):
    c.close()