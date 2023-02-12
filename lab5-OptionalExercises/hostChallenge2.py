import subprocess
import time

def receive_from_jtag():
    inputCmd = "nios2-terminal.exe"

    # subprocess allows python to run a bash command
    output = subprocess.Popen(inputCmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
    while True:
        line = output.stdout.readline().decode("utf-8") # read a line of the output from the terminal
        if line:
            print(line.strip()) # print the line if it is not empty
        else:
            break
        #time.sleep(0.1) # wait for 0.1 seconds before checking for new output again

def main():
    receive_from_jtag()
    
if __name__ == '__main__':
    main()
