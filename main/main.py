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
        if len(Server.messages) != 0:
            if Server.messages[len(Server.messages)-1] != lastmsg:
                print(Server.messages[len(Server.messages)-1])
                lastmsg = Server.messages[len(Server.messages)-1]

Server.StartServer()

threading.Thread(target=readServer).start()
while True:
    command = input()
    command = command.lower()
    if command in list(cmds.keys()):
        cmds[command]()
    else:
        Server.SendToServer(command)


