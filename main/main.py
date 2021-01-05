'''
This is a beta version of this software
'''
import subprocess
import os
import threading
import time

os.system("cls")

'''
This is hard coded for now
'''

executable = 'java -jar server.jar nogui'
minecraft_dir = (
    r'F:\Code\Python\New Projects\PyAdmin\server')


def server_command(cmd):
    global process
    process.stdin.write(bytes(cmd+"\n", "utf-8"))
    process.stdin.flush()

def readserver():
    global process
    while True:
        print(process.stdout.readline().decode('utf-8').strip("\n"))


os.chdir(minecraft_dir)
process = subprocess.Popen(executable, stdin=subprocess.PIPE, stdout=subprocess.PIPE)  # , stdout=subprocess.PIPE)
threading.Thread(target=readserver).start()

while True:
    command = input()
    command = command.lower()
    threading.Thread(target=server_command, args=((command,))).start()
    time.sleep(0.1)
