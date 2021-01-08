import main.api as api

Server = api.APIRequest()


def quitPy():
    Server.StopServer()


def returnStat():
    print(Server.Stats)


def restartServer():
    Server.RestartServer()


def startServer():
    Server.StartServer()
