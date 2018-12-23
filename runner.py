import threading
import os


def calling():
    os.system("behave")


for i in range(1, 200):
    threading.Thread(target=calling).start()



    # PRINT AND CHECK FULL
