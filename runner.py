import threading, time

def MainRunner():
    import main.main

def WebServer():
    import main.app

print("Starting webserver\n")
threading.Thread(target=WebServer).start()
time.sleep(1)
print("\n\n")
threading.Thread(target=MainRunner).start()
