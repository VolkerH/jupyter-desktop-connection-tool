from PySimpleGUI.PySimpleGUI import I, InputText
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

INITIAL = "Initial Setup"
HOST = "Hostname or IP"
KEY = "Private Keyfile"
USER = "Username"
CREATE = "Create Settingsfile"
DEFAULTIP = "127.0.0.1"


# Read settings
this_scripts_relpathstr = inspect.getfile(inspect.currentframe())
executable_path = Path("./") / this_scripts_relpathstr
settings_path = executable_path.parent / "connection_settings.json"


#############################
# Initial setup on first run
#############################
if not settings_path.exists():

    sg.popup("First start !", "Please setup the configuration in the next dialog")

    print(f"Default settings file not found: {str(settings_path)}")
    print("Creating a default settings file from user input.")

    setupgui = [
        [
            sg.Text(INITIAL),
        ],
        [sg.Text(HOST), sg.InputText(DEFAULTIP)],
        [sg.Text(USER), sg.InputText()],
        [sg.Text(KEY)],
        [sg.InputText(), sg.FileBrowse(file_types=(("All files", "*"),))],
        [sg.Button("Ok"), sg.Button("Cancel")],
    ]
    window = sg.Window(INITIAL, setupgui)
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == sg.WIN_CLOSED or event == "Cancel":
        print("Settings file creation cancelled")
    if event == "Ok":
        s = Settings()
        s.hostip = values[0]
        s.user = values[1]
        s.privatekeyfile = values[2]
        _save_settings_json(s, str(settings_path))

        sg.popup(
            f"Wrote configuration to {str(settings_path)}",
            "Restart the application for the settings to take effect",
        )

    exit()
else:
    s = _read_settings_json(str(settings_path))

##################################
# Normal GUI when config was found
##################################

layout = [
    [sg.Text("SpaceM Desktop Server Connection Tool")],
    [sg.Button(CONNECT)],
    [sg.Button(START)],
    [sg.Button(KILL)],
    [sg.Button(DISCONNECT)],
]

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
