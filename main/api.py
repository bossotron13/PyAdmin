'''
Scuffed but being worked on, will fix bad code later
'''
import os
import threading
import subprocess
import shlex
import sys
import time

class APIRequest:
    def __init__(self):
        self.alive = True
        self.AvalibleStats = {"Online, Accepting Players.": "Done (",
                              "Offline": "All chunks are saved", 
                              "Stopping Server": "Stopping the server",
                              "Starting Server": "Starting minecraft server version"}
        self.Stats = None
        self.messages = []
        self.mc = False
        self.dir = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + "/server"  # None

    def StartServer(self):
        os.chdir(self.dir)
        self.process = subprocess.Popen(shlex.split('java -jar -Xmx2G server.jar nogui'),
                                   stdin=subprocess.PIPE, stdout=subprocess.PIPE)  # , stdout=subprocess.PIPE)
        threading.Thread(target=self.ReadServer).start()
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
                        self.Stats = list(self.AvalibleStats.keys())[list(self.AvalibleStats.values()).index(x)]

    def SendToServer(self, cmd):
        if self.process.poll() == None:
            self.process.stdin.write(bytes(cmd+"\n", "utf-8"))
            self.process.stdin.flush()
        else:
            sys.exit()

    def RestartServer(self):
        self.StopServer()
        while self.mc:
            time.sleep(0.1)
        if not self.mc:
            self.StartServer()
            
    def RequestStatus(self):
        return self.Stats
    

'''
 I will efix configs later
 
    def ReadConfig(self):
        if not os.path.isfile('PyConfig.conf'):
            with open("PyAdmin.conf", "w") as f:
                f.close()
        else:
            with open("PyAdmin.conf", "r") as f:
                self.data = f.read()
    
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
