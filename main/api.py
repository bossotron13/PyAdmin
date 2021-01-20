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
        # List and Dict
        self.AvalibleStats = {"Online, Accepting Players": "Done (",
                              "Offline": "All chunks are saved",
                              "Stopping Server": "Stopping the server",
                              "Starting Server": "Starting minecraft server version"}
        self.CommandList = {"stop": ("Offline", self.StopServer),
                            "start": ("Online", self.StartServer),
                            "restart": ("Online", self.RestartServer)}
        self.ConfigDict = {}
        self.messages = []
        self.queue = []

        # Boolean values
        self.alive = True
        self.Stats = None
        self.questat = True
        self.mc = False

        # Strings
        self.dir = os.path.dirname(os.path.dirname(
            os.path.realpath(__file__))) + "/server"  # None
        self.ReadConfig()

    def StartServer(self):
        # Changes Dir so you can run java without path
        os.chdir(self.dir)

        # Starts the Java server
        self.process = subprocess.Popen(shlex.split('java -jar -Xmx2G server.jar nogui'),
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE)  # , stdout=subprocess.PIPE)
        
        # Starts to keep track of all server prints
        threading.Thread(target=self.ReadServer).start()

        # Starts the que system for the server
        threading.Thread(target=self.Que).start()

        # Says the java server has started
        self.mc = True

    def StopServer(self):
        # Sends a command to console to stop the server
        self.WriteToServer("stop")

    def RestartServer(self):
        # Stops server
        self.StopServer()

        # While java server is alive wait
        while self.mc:
            time.sleep(0.1)
            
        # If its not alive start new server
        if not self.mc:
            self.StartServer()
        
    def SendToServer(self, cmd):
        # Appends to the queue to add a command
        self.queue.append(cmd+"cmd")
    
    def SendCommand(self, cmd):
        self.queue.append(cmd+"func")

    def ReadServer(self):
        while True:
            # Message of the server logged and added to self.messages
            message = self.process.stdout.readline().decode('utf-8').strip("\n")
            self.messages.append(message)

            # Checks for any key words to determine the server state
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

    def WriteToServer(self, cmd):
        try:    # Checks if server is alive
            if self.process.poll() == None:
                # Writes to server then flushes
                self.process.stdin.write(bytes(cmd+"\n", "utf-8"))
                self.process.stdin.flush()
            else:
                sys.exit()
        except:
            return "Error"

    def Que(self):
        while True:
            # If anything is inside the queue list
            if self.queue:
                # If questat is True that means the queue is clear
                if self.questat:
                    self.questat = False
                    # Checks if write type then writes to the server what ever is in the queue list, pops it out
                    cmdType = "cmd" if 'cmd' in self.queue[0] else "func"
                    if cmdType == "cmd":
                        self.WriteToServer(self.queue.pop(0).strip('cmd'))
                        self.questat = True
                    else:
                        # Checks if its a func then calls Command list to see when it is finished executing
                        cmd = self.queue.pop(0).strip("func")
                        self.CommandList[cmd][1]()
                        while True:
                            if self.CommandList[cmd][0] in self.RequestStatus():
                                self.questat = True
                                break  
                            else:
                                time.sleep(0.1)


    def RequestStatus(self):
        # Returns server status
        return self.Stats
    
    def CreateConfig(self):
        # If config file doesnt exists, create it
        if not os.path.isfile("PyConfig.ini"):
            with open("PyConfig.ini", "w") as file:
                file.close()

    def WriteConfig(self, key, value):
        # If it exists else create
        if os.path.isfile("PyConig.ini"):
            with open("PyConfig.ini", "a") as file:
                # Writes key with value
                file.write(key + ":" + value + "\n")
        else:
            self.CreateConfig()

    def ReadConfig(self):
        if os.path.isfile("PyConfig.ini"):
            self.ConfigDict = {}
            with open("PyConfig.ini", "r") as file:
                lines = file.readlines()
                file.seek(0)
                # Creates a dictonary with all the keys and values into a dict
                for x in range(len(lines)):
                    data = file.readline().strip("\n").split(":")
                    self.ConfigDict[data[0]] = data[1]
        else:
            self.CreateConfig()

    def ReturnConfig(self):
        # Returns the config
        return self.ConfigDict
