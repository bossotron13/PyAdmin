import main.api as api

Server = api.APIRequest()

def quitPy():
    Server.StopServer()


def returnStat():
    Server.RequestStatus()


def restartServer():
    Server.RestartServer()


def startServer():
    Server.StartServer()
