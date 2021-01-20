import os, threading, time, sys
import main.definitions as definitions

Server = definitions.Server

cmds = {"/quit" : definitions.quitPy,
        "/stats" : definitions.returnStat,
        "/restart" : definitions.restartServer,
        "/start" : definitions.startServer}

def readServer():
    lastmsg = None
    while True:
        if Server.messages:
            if Server.RequestStatus() != "Offline" and " " not in Server.messages:
                for x in Server.messages:
                    print(Server.messages[Server.messages.index(x)])
                lastmsg = Server.messages[0]
                Server.messages.clear()
            else:
                Server.messages.clear()

Server.StartServer()

threading.Thread(target=readServer).start()
while True:
    command = input()
    command = command.lower()
    if command in list(cmds.keys()):
        cmds[command]()
    else:
        Server.SendToServer(command)


