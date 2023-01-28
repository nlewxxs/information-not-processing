# Information Processing Lab
Steven Shao, 27/01/2023

# Lab 1
## Task 0
Nothing special to talk about for the first part. Mainly for us to install Quartus.

## Task 1: 7-Segment LED Display
Following the steps from the guide pdf, we completed the 7-segment display. The four switches on the FPGA board are the input to the CPU and the HEX display is the output.

### Design flow of Quartus Project:

1. Creating verilog modules for the projects (submodules)
2. Creating top level module / combining submodules together 
>Remember to include submodules into the project
3. Pin assignment (A file is provided that all pins on the FPGA board are assigned) 
>Note: the name in the pin assignment file should be the names to use in the top level module. (e.g. SW for switches, HEX0 for the first display)
4. Compiling the file (a .sof file is produced when the compile is successful)
5. Tools/Programer: add the .sof inside the box and press start to download the project onto the board.

## Task 2
__Question 1: Explain what you find and link this back to the compilation report.__
![RTL_simple](./images/RTL_simple.png)
![compilation report](./images/comp_simple.png)

The graphical view of the synthesized design shows 4 inputs and 7 outputs (11 unconstrained ports/ 11 pins in total), which links to the compilation report.
>Q: what is Total logic elements?

__Question 2: Study the results of delay at differnet temperature and explain why?__
![delay](./images/delay.png)
Minimum propogation delay at 85C is given in the graph above. The report at other tempertures are unavailable due to technical issues. Expecting minimum timings to be higher for higher temperatures.

__Question 3: Create own design to display all 10-bit switches on three displays__
![top-level](./images/modified%20top%20level.png)

I mainly changed the top-level file to include 10-bit input SW and three 7-bit outputs HEX0/HEX1/HEX2. Keep in mind that the input and output names should match the pin assignment file. In addition, I implemented three hex-to-7seg and make sure the inputs to these submodules are the corresponding bits from SW. Since the input is only 10-bit, I concatenated the input to the last submodule with two 0s so that the input would be 4 bits as required.

![three displays](./images/three%20display.PNG)

The mapping:
![RTL_2](./images/RTL_2.png)

# Lab 2
## Task 1 Design a NIOS II System
![NIOS1](./images/nios1.png)
![NIOS2](./images/nios2.png)

In task 1, we use Plat Designer Tools in Quartus. Inside the tools, we can use the pre-existing subblocks to assemble a processor. 

* `clk` is a fixed block in every design. It contains the clk and reset line, which are connected with all other synchronous components

* `cpu` Nios II CPU has `data_master`, which is used to communicate with other software components. `instruction_master`is connected with onchip memory, because all instructions are stored inside the memory.

* `jtag_uart` is a debug component, which seems to show any error on the PC terminal using UART protocol. The protocol is a one to one communication method. It uses the USB cable to communicate.

* `switch` `led` `HEX0` etc. are PIOs, hardware components on the FPGA board.

* `external port` are used to connect the outputs to higher level design.

### Design flow of NIOS II System:
1. Drag all components into the design (CPU, Memory, PIOs ...)
2. Connect all lines among all related components
3. `System/Assign Base Address`
> Don't know what base address means?
4. Save as a `.qsy` file
5. Right click `cpu` and `select Vectors` tab, set `reset vector memory` and `exception vector memory` to `onchip_memory.s1`
6. Save the design and click on `Generate HDL`
> HDL: hardware description language: `.v`file, auto-generated from `.qsy`, which contains the description of top-level connections.

### Defining pins:
The HDL file `nios_setup_inst.v` generated the top level connection code that should copy into the top file and modify to match the defined output names inside the top files.

![v file](./images/v%20file.PNG)
![top HDL](./images/top%20HDL.PNG)

After that, we can compile the qsy file. This will generate a `.sof` file which can then input into the FPGA board.

## Task 2 Software Design
Use `Tools/Nios II Software build tools for Eclipse` to code our software design in C.

### Software Programming Work Flow:
1. Open Eclipse and Create new `Nios II Application and BSP from Template`
2. Navigate to click on the `.sopcinfo `
> `.sopcinfo` file is generated from `.qsy` design, which includes the corresponding include file that can be used in the software design file?
3. Select `Hello_World_Small`. The small project make sureenough memory in FPGA
4. Change `hello_world_small.c` to any `.c` file we like to implement.
5. Right click `hello_world_small_bsp` and select `Generate BSP`
6. Right click `hello_world_small` and select `Build Project`
7. A `.elf` file will generate after successful building process. This file is saved under `/home/lab/task/software/hello_world_small`.

This is the `.c` file we would like to run on Nios II processor:

![Hello C](./images/hello%20C.PNG)

The program will print "Hello from Nios II!" on the terminal. LED will turn on when button is pressed.

> ? quite not understanding what the code inside the file means ? 

### Downloading the Program and show on PC terminal
In this task, we will run the following .c program in Nios II processor.
1. Open Nios shell from `.bat file` located inside the folder where Nios II is installed in the first place.
> The instruction pdf said to open from terminal by typing shell is only available for linux, not windows
2. Go to the directory where the project is located `cd .../software/hello_word_sw` and type in `nios2-download -g hello_world_sw.elf`. This downloads the .elf file onto the FPGA board to run the compiled C code on the NIOS II processor.
3. Open another terminal and type in `nios2-terminal` to open up a terminal window connected to the nios2.
4. The program will now run on the second terminal

This is what we got aftering following through the step: (Hello from Nios II!)

![Hello NIOS](./images/hello%20NIOS.png)

The LED is lighting up when the button is pressed:

![LED NIOS](./images/LED%20NIOS.jpg)