import paramiko
import time
import re
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Settings:
    hostip: str = "10.11.19.188"
    user: str = "spacem"
    privatekeyfile: str = "/home/hilsenst/.ssh/id_rsa"
    docker_start_cmd: str = "/etc/spacem_jupyter_desktop/rundocker.sh"
    docker_stderr_cmd: str = "/usr/bin/cat $HOME/.jupyter_docker_stderr"
    docker_port_cmd: str = "/usr/bin/cat $HOME/.jupyter_docker_port"
    docker_kill_cmd: str = "/usr/bin/killall docker"
    server_startup_time: int = 5


def get_ssh_client_and_key(s: Settings):
    k = paramiko.RSAKey.from_private_key_file(s.privatekeyfile)
    c = paramiko.SSHClient()
    c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    return c, k


def connect(c, pkey, s: Settings):
    c.connect(hostname=s.hostip, username=s.user, pkey=pkey)


def start_server(c, s: Settings):
    stdin, stdout, stderr = c.exec_command(s.docker_start_cmd)
    time.sleep(s.server_startup_time)  # give server some time to start up

    # Jupyterlab sends connection URL to stderr, which
    # we redirect into a file in the startup script on
    # the server.
    stdin, stdout, stderr = c.exec_command(s.docker_stderr_cmd)
    catout = stdout.read()
    for line in catout.decode("utf-8").split("\n"):
        m = re.match(r".*(?P<token>\?token=.+)", line)
        if m is not None:
            break
    token = m["token"]

    # The startup script on the server looks for an
    # available port number and redirects it into a file
    stdin, stdout, stderr = c.exec_command(s.docker_port_cmd)
    port = stdout.read().decode("utf-8").strip()

    jupyterURL = f"http://{s.hostip}:{port}/{token}"
    return jupyterURL


def kill_server(c, s: Settings):
    c.exec_command(s.docker_kill_cmd)


def disconnect(c):
    c.close()


def _save_settings_json(s: Settings, filename: str) -> None:
    from json import dump

    with open(filename, "w") as f:
        dump(s.to_json(), f, sort_keys=True, indent=4)


def _read_settings_json(filename: str) -> Settings:
    from json import load

    with open(filename, "r") as f:
        s = Settings.from_json(load(f))
    return s


# Tests
def test_settings():
    from json import dumps

    s = Settings()
    f = "tmp_test.json"
    _save_settings_json(s, f)
    reload = _read_settings_json(f)
    assert dumps(s.to_json(), sort_keys=True) == dumps(reload.to_json(), sort_keys=True)
