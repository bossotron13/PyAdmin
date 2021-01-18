'''
Scuffed but being worked on, will fix bad code later
'''
import os
import threading
import subprocess
import shlex
import sys
import time
import psutil


class APIRequest:
    def __init__(self):
        self.alive = True
        self.AvalibleStats = {"Online, Accepting Players.": "Done (",
                              "Offline": "All chunks are saved",
                              "Stopping Server": "Stopping the server",
                              "Starting Server": "Starting minecraft server version"}
        self.Stats = None
        self.messages = []
        self.queue = []
        self.questat = True
        self.mc = False
        self.dir = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + "/server"  # None

    def StartServer(self):
        os.chdir(self.dir)
        self.process = subprocess.Popen(shlex.split('java -jar -Xmx2G server.jar nogui'),
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)  # , stdout=subprocess.PIPE)
        threading.Thread(target=self.ReadServer).start()
        threading.Thread(target=self.Que).start()
        self.mc = True

    def StopServer(self):
        self.SendToServer("stop")

    def ReadServer(self):
        while True:
            message = self.process.stdout.readline().decode('utf-8').strip("\n")
            self.messages.append(message)
            for x in list(self.AvalibleStats.values()):
                if x in message:
                    if x == self.AvalibleStats["Offline"]:
                        while self.mc:
                            if self.process.poll() != None:
                                self.Stats = list(self.AvalibleStats.keys())[
                                    list(self.AvalibleStats.values()).index(x)]
                                self.mc = False
                    else:
                        self.Stats = list(self.AvalibleStats.keys())[
                            list(self.AvalibleStats.values()).index(x)]

    def SendToServer(self, cmd):
        self.queue.append(cmd)

    def Que(self):
        while True:
            if self.queue:
                print("Test")
                if self.questat:
                    self.questat = False
                    self.WriteToServer(self.queue.pop(0))
                    currentStat = self.Stats
                    while not self.questat:
                        if currentStat != self.Stats:
                            time.sleep(2)
                            self.questat = True
                            break
                elif self.questat and self.process.poll() != None:
                    self.questat = False
                elif not self.questat and self.process.poll() == None:
                    self.questat = True

    def WriteToServer(self, cmd):
        try:
            if self.process.poll() == None:
                self.process.stdin.write(bytes(cmd+"\n", "utf-8"))
                self.process.stdin.flush()
            else:
                sys.exit()
        except:
            return "Error"

    def RestartServer(self):
        self.StopServer()
        while self.mc:
            time.sleep(0.1)
        if not self.mc:
            self.StartServer()

    def RequestStatus(self):
        return self.Stats


'''
    def ReadConfig(self):
        print(os.path.isfile)
        if not os.path.isfile('PyConfig.conf'):
            with open("PyAdmin.conf", "w") as f:
                f.close()
        else:
            with open("PyAdmin.conf", "r") as f:
                self.data = f.read()
                return self.data
    
    def WriteConfig(self, write, value):
        if not os.path.isfile('PyConfig.conf'):
            with open("PyAdmin.conf", "w") as f:
                f.close()
        if os.path.isfile('PyConfig.conf'):
            with open("PyAdmin.conf", "a") as f:
                if not write in f.read():
                    f.write(write + ":" + value)
                else:
                    return "Value already exists"
'''
