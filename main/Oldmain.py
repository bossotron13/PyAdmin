'''
This is a beta version of this software
'''
import subprocess
import os
import threading
import time
import shlex
import platform


if platform.system() == "Windows":
    def clear():
        os.system("cls")
else:
    def clear():
        os.system("clear")

clear()


'''
This is hard coded for now
'''

minecraft_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "/server" # This will go back one more directory for testing
print(minecraft_dir)


def server_command(cmd):
    global process
    process.stdin.write(bytes(cmd+"\n", "utf-8"))
    process.stdin.flush()

def readserver():
    global process
    while True:
        print(process.stdout.readline().decode('utf-8').strip("\n"))


os.chdir(minecraft_dir)
process = subprocess.Popen(shlex.split('java -jar -Xmx2G server.jar nogui'), stdin=subprocess.PIPE, stdout=subprocess.PIPE)  # , stdout=subprocess.PIPE)
threading.Thread(target=readserver).start()

while True:
    command = input()
    command = command.lower()
    threading.Thread(target=server_command, args=((command,))).start()
    time.sleep(0.1)
