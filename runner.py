import threading, time, multiprocessing

def MainRunner():
    import main.main

def WebServer():
    import main.website.app

def SetServer():
    import main.definitions as holder
    import main.website.ApiShare as server
    server.SetApi(holder.Server)

if __name__ == "__main__":
    threading.Thread(target=SetServer).start()
    time.sleep(1)
    print("Starting webserver\n")
    threading.Thread(target=WebServer).start()
    time.sleep(1)
    print("\n\n")
    threading.Thread(target=MainRunner).start()
