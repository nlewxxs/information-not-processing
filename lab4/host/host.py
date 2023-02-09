import time
import threading
import readchar
from pexpect.popen_spawn import PopenSpawn as newprocess
import pexpect
import shutup
import os

control = str # init a global, not too concerned about memory on the host side. 

def get_input():
    global control
    while True:
        control = str(readchar.readchar())
        time.sleep(0.1)    

def main():

    shutup.please() # blocks deprecation warnings

    os.system("echo 'NIOS II Host Controller' | lolcat -F 0.6")
    print("-----------------------------------------------\n")
    print("Press 1 to enable filtering, 0 for raw accelerometer data. Press q to quit\n")
    print("-----------------------------------------------\n")

    global control
    control = "a"

    process = newprocess('nios2-terminal') # init the nios2-terminal shell

    t2 = threading.Thread(target=get_input) # init the character reading thread
    t2.setDaemon(True) # shouldn't prevent program from closing
    t2.start()

    while True:
        if control in ['0', '1']:
            print(">> sending control signal: " + control)
            for i in range(5):
                process.send(control)    # send a pulse of 5 control signals just in case
                time.sleep(0.1)
            control = 'a'            # reset to usual value
        elif control == 'q':
            return 0
        else:
            process.send('a')
            time.sleep(0.1)     

if __name__ == '__main__':
    main()
