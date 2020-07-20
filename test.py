import threading



def fun():
    print(True)
threading.Thread(target=fun).start()

