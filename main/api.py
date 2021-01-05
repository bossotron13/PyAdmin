'''
Scuffed but being worked on, will fix bad code later
'''

class APIRequest:
    def __init__(self):
        self.alive = True
        self.AvalibleStats = {"Online, Accepting Players.": "Done (",
                              "Offline": "All chunks are saved", 
                              "Stopping Server": "Stopping the server",
                              "Starting": "Starting minecraft server version"}
        self.Stats = None
        self.messages = []

    def StartServer(self):
        self.Stats = list(self.AvalibleStats.keys())[0]  
    
    def StopServer(self):
        self.Stats = list(self.AvalibleStats.keys())[2]
        self.mc = False

    def ReadServer(self):
        while True:
            message = process.stdout.readline().decode('utf-8').strip("\n")
            self.messages.append(message)
            for x in list(self.AvalibleStats.values()):
                if x in message:
                    self.Stats = self.AvalibleStats[list(
                        self.AvalibleStats.values()).index(x)]
    
    def SendToServer(self,  cmd):
        process.stdin.write(bytes(cmd+"\n", "utf-8"))
        process.stdin.flush()

    def RestartServer(self):
        pass

    def ReadConfig(self):
        pass
    
    def RequestStatus(self):
        pass
    
