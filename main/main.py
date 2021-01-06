import api, os, threading, time, sys

Server = api.APIRequest()

def quitPy():
    Server.StopServer()

def returnStat():
    print(Server.Stats)

def restartServer():
    Server.RestartServer()

def startServer():
    Server.StartServer()

cmds = {"/quit" : quitPy,
        "/stats" : returnStat,
        "/restart" : restartServer,
        "/start" : startServer}

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


