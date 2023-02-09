import subprocess
import time
import readchar
import threading
import shutup
import signal
import os
import errno
import re

# initialising global variables
control = str  # current keystroke
nios = subprocess.Popen('nios2-terminal', shell=True, executable='/bin/bash', stdout=subprocess.PIPE, stdin=subprocess.PIPE, preexec_fn=os.setsid)  # niosterminal
show_data = False  # display accelerometer data on screen?
pause = False  # pause input reading thread
coeffs_received = False  # has the de-10 accepted the coefficients?


class BadCoefficientExemption(Exception):
    # exception for if coefficient input doesn't match regex
    pass


def send_on_jtag(cmd):
    """
    :param str cmd: command to be encoded

    Encodes a command using UTF-8 and sends it along JTAG_UART
    """
    global nios

    try:
        nios.stdin.write(cmd.encode('utf-8'))
    # IOError = not connected, or likewise
    except IOError as e:
        if e.errno != errno.EPIPE and e.errno != errno.EINVAL:
            raise

    nios.stdin.flush()  # stdin must be flushed otherwise commands are not sent
    

def read_from_shitty_terminal():
    """Run as a daemon thread.

    Stdout buffer must constantly be cleared, otherwise you will end up
    with a very long queue of outputs in front of the one you want to read
    """
    global show_data
    global coeffs_received

    while True:
        try:
            # Read a line from nios2-terminal
            reading = nios.stdout.readline().decode('utf-8')
        except UnicodeError: 
            # this occasionally occurs, not critical so ignore.
            continue 
        
        inp = reading.strip() # input without whitespace
        first = inp.split()[0].strip()  # first word of input

        if (inp != ""):
            if inp.split()[0] == 'y':
                # accelerometer data is outputted as "y value: {y}"
                if show_data:
                    # accel data is only shown if the boolean is True (controlled by 'd' on keyboard)
                    print(reading,)
            elif first != '<-->': # don't want to see this in the output, mainly for debugging
                print(reading,) # comma means no newline
            if first == "<UPDATED_COEFFICIENTS>": 
                # this is the format of de-10's reply to coefficient change
                coeffs_received = True
            else:
                coeffs_received = False


def get_input():
    """Run as a daemon thread.

    This uses the readchar library to intercept any characters pressed on the keyboard
    so they don't directly go into the nios2-terminal!!
    So we can process the character first and then manually send something using send_on_jtag()
    """
    global control
    global pause

    while not pause:
        control = str(readchar.readchar())
        time.sleep(0.1)  # small delay can be afforded to give other functions processing time


def send_coeffs():
    """
    Takes coefficients as input from user, performs brief validation and sends coefficients to the DE-10
    """

    global nios
    global coeffs_received

    stream = []  # message stream to be sent across

    # prompt input and split using commas as the delimiter
    coeffs_input = input('\nPlease enter new coefficients, separated by commas\n\n>>> ')
    new_coeffs = coeffs_input.split(sep=',')

    for coefficient in new_coeffs:
        if not re.match("^[+-]?((\d+(\.\d+)?)|(\.\d+))$", coefficient.strip()):
            # regex for decimals, courtesy of some goblin on stackoverflow so don't ask me to decipher it
            raise BadCoefficientExemption
        for char in coefficient:
            if char != ' ':
                # we only append non-space characters to the stream.
                stream.append(char)
        # commas are put back in as a delimiter for the DE-10 (so it knows where each coefficient stops)
        stream.append(',')

    print("\nMESSAGE STREAM:\n", stream)
    send_on_jtag('c')  # signals to DE-10 to prepare for coefficient transmission
    time.sleep(2)
    print('starting transmission....')

    for digit in stream:
        send_on_jtag(digit)
        print('HOST >> sending ' + digit)
        time.sleep(0.4)  # slight increase to delay just because we want 100% accuracy here
    print("end of transmission\n\n")
    send_on_jtag('x')  # signals to the DE-10 that all characters have been sent

    timeout = time.time() + 3  # 3 second timeout
    while True:
        if time.time() > timeout:
            break  # DE-10 did not respond in time
        elif coeffs_received:
            return True
    return False


def main():

    shutup.please() # removes software deprecation warnings

    global control
    global show_data  # i know this is bad i dont care
    global nios
    global pause
    global coeffs_received
    
    for i in range(3):
        # removes the nios welcome message from the stdout buffer
        nios.stdout.readline().decode('iso-8859-1')
        # iso-8859-1 prevents a UnicodeError from being raised by the nios message
    
    # display welcome message
    # note that the 'lolcat' package is just for rainbow font
    # either install or change the lines to plain print lines
    os.system("echo '\nNIOS II Host Controller' | lolcat -F 0.8")
    os.system('echo "------------------------------------------------------\n" | lolcat -F 0.8')
    print("Press 1 to enable filtering, 0 for raw accelerometer data. \nPress 'd' to toggle data transfer \nPress 'c' to update coefficients \nPress 'q' to quit\n")
    os.system('echo "------------------------------------------------------" | lolcat -F 0.8')
    time.sleep(0.2)

    # clearing buffer again because sometimes a few accelerometer values slip in
    nios.stdout.readline().decode('iso-8859-1')
    nios.stdout.readline().decode('iso-8859-1')

    # Start terminal reading thread (this runs in parallel to everything)
    readings = threading.Thread(target=read_from_shitty_terminal)
    readings.setDaemon(True) # signifies that we don't wait for it to finish, once main() is done then all daemons are killed
    readings.start()

    # Start user input grabber, as above
    inputs = threading.Thread(target=get_input)
    inputs.setDaemon(True)
    inputs.start()

    # if the below message doesn't show up then you have either a BrokenPipeError or something else wrong with jtag.
    # usually caused by incorrect termination of the program, i.e. using Ctrl^C or an unexpected error.
    # Unplug board, reblast, reprogram. 

    print('daemons set up and buffer cleared. terminal session active.\n')

    while True:
        if control in ['0', '1']:  # 1 = filtered data, 0 = raw
            print(">> sending control signal: " + control)
            for i in range(5):
                send_on_jtag(control)  # send a pulse of 5 control signals just in case
                time.sleep(0.1)
            control = 'a'  # reset to default value. 

        elif control == 'q':  # correct way to terminate program
            break

        elif control == 'd':
            show_data ^= True  # toggle display of accelerometer data 
            control = 'a'  # reset to default

        elif control == 'c':
            # pause everything and call send_coeffs
            show_data = False  # avoiding nios2-terminal diarrhoea as soon as process finishes
            pause = True
            try:
                coeffs_sent = send_coeffs()
            except BadCoefficientExemption:  # incorrect input
                print('Please adhere to the input rules.\n')

            if coeffs_received:
                time.sleep(0.2)
                os.system(r'echo "Coefficients accepted by Altera MAX 10 board" | lolcat -F 0.8')
                print("terminal session resumed")
                print("------------------------------------------------------\n")
                control = 'a' # resetting
                coeffs_received = False

                pause = False  # resume execution of program

                # input thread must be manually re-declared and restarted (can't call .start() twice)
                inputs = threading.Thread(target=get_input)
                inputs.setDaemon(True)
                inputs.start()

            else:
                print("coefficient update timed out :(")
                break
        else:
            send_on_jtag('a')  # spam a by default - otherwise the c program hangs on 'prompt=getc(fp)'
            time.sleep(0.1)   

    # send KILL signal for the nios2terminal subprocess initiated at the start
    os.killpg(os.getpgid(nios.pid), signal.SIGTERM)   
    
if __name__ == '__main__':
    main()
