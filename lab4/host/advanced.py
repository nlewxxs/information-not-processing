import subprocess
import time
import readchar
import threading
import shutup
import signal
import os
import errno
import re

control = str # init a global, not too concerned about memory on the host side. 
nios = subprocess.Popen('nios2-terminal', shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stdin=subprocess.PIPE, preexec_fn=os.setsid)
show_data = False
pause = False
coeffs_received = False

class BadCoefficientExemption(Exception):
    pass

def send_on_jtag(cmd):
    global nios
    try:
        nios.stdin.write(cmd.encode('utf-8'))
    except IOError as e:
        if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
            raise
    # subprocess allows python to run a bash command

    nios.stdin.flush() # idfk
    
def read_from_shitty_terminal():
    # this needs to always be running to constantly be clearing the buffer 
    global show_data
    global coeffs_received
    while True:
        try:
            reading = nios.stdout.readline().decode('utf-8')
        except UnicodeError:
            continue 
        inp = reading.strip()
        first = inp.split()[0].strip()
        if (inp != ""):
            if inp.split()[0] == 'y':
                if show_data:
                    print(reading,)
            elif first != '<-->': # don't want to see this in da output
                print(reading,)
            if first == "<UPDATED_COEFFICIENTS>":
                coeffs_received = True


def get_input():
    global control
    global pause
    while not pause:
        control = str(readchar.readchar())
        time.sleep(0.1)


def send_coeffs():
    global nios
    global coeffs_received
    stream = []
    coeffs_input = input('\nPlease enter new coefficients, separated by commas and with no spaces\n\n>>> ')
    new_coeffs = coeffs_input.split(sep=',')
    # stream.append(str(len(new_coeffs))) # first value is number of coeffs, c needs this to init an array.
    # This way we can convert between different number of taps. 
    for coefficient in new_coeffs:
        if not re.match("^[+-]?((\d+(\.\d+)?)|(\.\d+))$", coefficient.strip()):
            # regex for decimals, courtesy of some goblin on stackoverflow so don't ask me to decipher it
            raise BadCoefficientExemption
        for char in coefficient:
            if char != ' ':
                stream.append(char)
        stream.append(',')
    print("MESSAGE STREAM:\n", stream)
    send_on_jtag('c')
    time.sleep(2)
    print('initiating transmission....')
    for digit in stream:
        send_on_jtag(digit)
        print('HOST: sending ' + digit)
        time.sleep(0.8) # slight increase to delay just bc we want 100% accuracy here
        # indicating end of transmission
    print("end of transmission\n\n")
    send_on_jtag('x')

    timeout = time.time() + 5 # 5 second timeout
    while True:
        if time.time() > timeout:
            break # fpga did not respond in time
        elif coeffs_received:
            return True
    return False

def main():
    
    shutup.please()

    global control
    global show_data    # i know this is bad i dont care
    global nios
    global pause
    global coeffs_received
    
    for i in range(3):
        # removes the nios welcome message from the stdout buffer
        nios.stdout.readline().decode('iso-8859-1')
        # iso-8859-1 prevents a UnicodeError from being raised by the nios message
    
    os.system("echo '\nNIOS II Host Controller' | lolcat -F 0.8")
    os.system('echo "------------------------------------------------------\n" | lolcat -F 0.8')
    print("Press 1 to enable filtering, 0 for raw accelerometer data. \nPress 'd' to toggle data transfer \nPress 'q' to quit\n")
    os.system('echo "------------------------------------------------------" | lolcat -F 0.8')
    time.sleep(0.2)

    # clearing buffer because sometimes a few accelerometer values slip in
    nios.stdout.readline().decode('iso-8859-1')
    nios.stdout.readline().decode('iso-8859-1')

    readings = threading.Thread(target=read_from_shitty_terminal)
    readings.setDaemon(True)
    readings.start()

    inputs = threading.Thread(target=get_input)
    inputs.setDaemon(True)
    inputs.start()

    print('daemons set up and buffer cleared. \n')

    while True:
        if control in ['0', '1']:
            print(">> sending control signal: " + control)
            for i in range(5):
                send_on_jtag(control)       # send a pulse of 5 control signals just in case
                time.sleep(0.1)
            control = 'a'                   # reset to usual value
        elif control == 'q':
            break
        elif control == 'd':
            show_data ^= True # toggle display of accelerometer data 
            control = 'a' # set it back to prevent wibble wobble 
        elif control == 'c':
            # pause everything. 
            show_data = False # avoiding terminal diarrhoea
            pause = True
            try:
                coeffs_sent = send_coeffs()
            except BadCoefficientExemption:
                print('input bad')
            if coeffs_sent:
                print("coefficients acknowledged by altera board")
                control = 'a' # resetting
                coeffs_received = False

                pause = False
                inputs = threading.Thread(target=get_input)
                inputs.setDaemon(True)
                inputs.start()
            else:
                print("coefficient update timed out :(")
                break
        else:
            send_on_jtag('a')
            time.sleep(0.1)   

    os.killpg(os.getpgid(nios.pid), signal.SIGTERM)  # housekeeping   
    
if __name__ == '__main__':
    main()

# TODO: make y auto update instead of printing newline each time

# TODO: change the coeffs
