# Receiving end for FPGA communication
import subprocess
import time
import readchar
import os
import errno
import sys
import threading
import signal

class FpgaNoResponse(Exception):
    pass

class Connection:

    def __init__(self) -> None:
        self._nios = subprocess.Popen('nios2-terminal', shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stdin=subprocess.PIPE, preexec_fn=os.setsid)
        self._control = ""
        self._reading = ""
        self._comms = True
    

    def send_on_jtag(self, cmd : str) -> None:
        try:
            self._nios.stdin.write(cmd.encode('utf-8'))
        except IOError as e:
            if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
                raise
        # print("sending >> " + cmd)
        self._nios.stdin.flush()


    def read_from_terminal(self) -> None:
        while True:
            try: 
                self._reading = self._nios.stdout.readline().decode('utf-8')
            except UnicodeError:
                continue
        
            # inp = self._reading.strip()

            # if (inp != "") and self._show_data:
            #     print(self._reading,)
    
    def get_input(self) -> None:

        while True:
            self._control = str(readchar.readchar())
            time.sleep(0.1)
    
    def init_connection(self) -> None:
        for i in range(3):
            self._nios.stdout.readline().decode('iso-8859-1')
            # clears nios2 terminal welcome message from stdout buffer
            # iso-8859-1 prevents UnicodeDecodeError (some weird character being sent by nios)

        os.system("echo '\nNIOS II Host Controller'")
        os.system('echo "------------------------------------------------------\n"')
        print("Press 1 to enable filtering, 0 for raw accelerometer data. \nPress 'd' to toggle data transfer \nPress 'c' to update coefficients \nPress 'q' to quit\n")
        os.system('echo "------------------------------------------------------"')
        time.sleep(0.2)

        readings = threading.Thread(target=self.read_from_terminal)
        readings.daemon = True
        readings.start()

        inputs = threading.Thread(target=self.get_input)
        inputs.daemon = True
        inputs.start()

        print('daemons set up and buffer cleared. terminal session active.\n')


class FPGA(Connection):
    def __init__(self) -> None:
        super().__init__()
        self._score = "2468"
        print(list(self._score))
    
    def communicate(self) -> None:
        while self._comms:
            if self._control == "q":
                self._comms = False
                break
            # if self._control in ['0', '1']:
            #     print('>> sending control signal: ' + self._control)
            #     for i in range(3):
            #         self.send_on_jtag(self._control)
            #         time.sleep(0.1)
            #     self._control = 'a'

            # elif self._control == 'q':
            #     break

            # elif self._control == 'd':
            #     self._show_data ^= True # toggle
            #     self._control = 'a' # reset to default
            
            # else:
            myscore = list(self._score)
            self.send_on_jtag('s')
            time.sleep(0.1)
            self.send_on_jtag(myscore[0])
            time.sleep(0.1)
            self.send_on_jtag(myscore[1])
            time.sleep(0.1)
            self.send_on_jtag(myscore[2])
            time.sleep(0.1)
            self.send_on_jtag(myscore[3])
            time.sleep(0.1)

        os.killpg(os.getpgid(self._nios.pid), signal.SIGTERM)
    
    def start_communication(self) -> None:

        self.init_connection()

        com = threading.Thread(target=self.communicate)
        com.daemon = True
        com.start()
    
    def read(self) -> str:
        return self._reading

    def kill(self) -> None:
        os.killpg(os.getpgid(self._nios.pid), signal.SIGTERM)        
    
    # def send_result(self, win : bool, score : str) -> None:
    #     self._comms = False
    #     result = 'W' if win else 'L'
    #     self.send_on_jtag(result) # sends win or loss, prepares for score transmission

    #     for i in list(score):
    #         time.sleep(0.2)
    #         self.send_on_jtag(i)
        
    #     time.sleep(0.2)
    #     self.send_on_jtag('d') # done

    #     sendtime = time.time()
    #     while time.time() < sendtime + 2:
    #         if self._reading == "d":  # received by fpga, confirmed
    #             self._comms = True  # restart thread, new object required
    #             com = threading.Thread(target=self.communicate)
    #             com.daemon = True
    #             com.start()
    #             break      
        
        #raise FpgaNoResponse # fpga did not confirm

    def update_score(self, score : str) -> None:
        self._score = score   

if __name__ == "__main__":

    fpga = FPGA()               # init a new FPGA instance
    fpga.start_communication()  # initialise communication
    # fpga.read()                 # get reading at that point in time
    while fpga._control != 'q':
        print(("reading: " + fpga.read()),)
        # time.sleep(0.1))
        # fpga.send_result(True, "2222")
    fpga.kill()
    # fpga.send_result(True, '0230')


            

