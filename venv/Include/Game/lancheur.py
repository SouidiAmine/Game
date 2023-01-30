import threading
import os

def run_command(command):
    os.system(command)


command1 = "python main.py"
command2 = "python main2.py"

thread1 = threading.Thread(target=run_command, args=(command1,))
thread2 = threading.Thread(target=run_command, args=(command2,))


thread1.start()
thread2.start()


thread1.join()
thread2.join()
