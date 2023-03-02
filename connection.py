# Receiving end for FPGA communication
import subprocess
import time
import readchar
import os
import errno
import threading
import signal

class Connection:

    def __init__(self) -> None:
        self._nios = subprocess.Popen('nios2-terminal', shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stdin=subprocess.PIPE, preexec_fn=os.setsid)
        self._show_data = False
        self._control = ""
        self._reading = ""
    
    def send_on_jtag(self, cmd : str) -> None:
        try:
            self._nios.stdin.write(cmd.encode('utf-8'))
        except IOError as e:
            if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
                raise

        self._nios.stdin.flush()

    def read_from_terminal(self) -> None:
        while True:
            try: 
                self._reading = self._nios.stdout.readline().decode('utf-8')
            except UnicodeError:
                continue
        
            inp = self._reading.strip()

            try:
                first = inp.split()[0].strip()
            except IndexError:
                first = ''

            if (inp != "") and self._show_data:
                print(self._reading,)
    
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
        self._action = ""
    
    def communicate(self) -> None:
        while True:
            if self._control in ['0', '1']:
                print('>> sending control signal: ' + self._control)
                for i in range(3):
                    self.send_on_jtag(self._control)
                    time.sleep(0.1)
                self._control = 'a'

            elif self._control == 'q':
                break

            elif self._control == 'd':
                self._show_data ^= True # toggle
                self._control = 'a' # reset to default
            
            else:
                self.send_on_jtag('a')
                time.sleep(0.1)

        os.killpg(os.getpgid(self._nios.pid), signal.SIGTERM)
    
    def start_communication(self) -> None:

        self.init_connection()

        comms = threading.Thread(target=self.communicate)
        comms.daemon = True
        comms.start()
    
    def read(self) -> str:
        return self._reading

    def kill(self) -> None:
        os.killpg(os.getpgid(self._nios.pid), signal.SIGTERM)

if __name__ == "__main__":

    fpga = FPGA()               # init a new FPGA instance
    fpga.start_communication()  # initialise communication
     Updated upstream
    #fpga.read()                 # get reading at that point in time

    while True:
        print(fpga.read())

    while True:
        print(fpga.read())
            

