from ssh_connect import *
from ssh_connect import _save_settings_json, _read_settings_json
from pathlib import Path
import inspect
import PySimpleGUI as sg
import webbrowser

CONNECT = "Connect to Server"
START = "Start Jupyter Desktop"
KILL = "Kill Jupyter Desktop"
DISCONNECT = "Disconnect"

layout = [
    [sg.Text("SpaceM Desktop Server Connection Tool")],
    [sg.Button(CONNECT)],
    [sg.Button(START)],
    [sg.Button(KILL)],
    [sg.Button(DISCONNECT)],
]


# Read settings
this_scripts_relpathstr = inspect.getfile(inspect.currentframe())
executable_path = Path("./") / this_scripts_relpathstr
settings_path = executable_path.parent / "connection_settings.json"

if not settings_path.exists():
    print(f"Default settings file not found: {str(settings_path)}")
    print("Creating a default settings file from template.")
    print("Please modify with your username and private key file path")
    s = Settings()
    _save_settings_json(s, str(settings_path))
    exit()
else:
    s = _read_settings_json(str(settings_path))

# Create the window
window = sg.Window("Connection tool", layout)
c, k = get_ssh_client_and_key(s)

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED:
        break
    if event == CONNECT:
        print("Connecting to server")
        connect(c, k, s)
    if event == START:
        print("Sarting Jupyter")
        URL = start_server(c, s)
        webbrowser.open(URL, new=1)
        print(URL)
    if event == KILL:
        print("Killing Server")
        kill_server(c, s)
    if event == DISCONNECT:
        print("Disconnecting")
        disconnect(c)

window.close()
