# Information Processing Labs
#### Nik Lewis, 19/01/2023

# Lab 1

Basic hex to seg display.

![lab1mapview](/images/lab1mapview.png)

Linking to the compilation report, you can see that we have 4 `Unconstrained Input Ports` and 7 `Unconstrained Output Ports`.

The total number of port paths is _28_ = _7 * 4_. Note that the total input and output port paths are the same because all inputs and outputs go through the same single `hex_to_7seg` block.

---

### Temperature Dependency

Quartus only lets me change temperature between 85C and 0C, minimum propogation delay seems to be the same??

> Fix above, why is this the case? Expecting minimum timings to be higher for higher temperatures.

---

### Extending to 3 hex displays

![lab1task2](/images/lab1fpga.png)

Note here that the maximum number displayed is 3FF since there are only 10 pins.

Code modifications are as follows. For the last seg display, I concatenated the switches with two 0s so that the input would be 4 bits as required.  

![lab1task2top](/images/lab1task2top.png)

> Note that SEG0, SEG1 and SEG3 are variables storing the values of HEX0, HEX1 and HEX2. This is why the accidental typo (SEG3 should be SEG2) makes no difference, as it is still mapped to the HEX2 pin.

And the mapping changes:

![lab1task2mapping](/images/lab1task2map.png)

![compiler_report](/images/lab1task2compreport.png)

Upon inspection of the compilation report, we see that there are:

* 10 _input ports_, obviously because there are 10 switches
* 20 _output ports_, this is because I extended the HEX2 value in order to fit it into the hex_to_7seg function. I suppose this makes it "constrained".
* 66 paths, because ( 4 * 7 ) + ( 4 * 7 ) + ( 2 * 4 ) + ( 1 * 2 ) = 66

> This is just based off the diagram, it doesn't fully make sense to me. which of the last ones are unconstrained? what is going on here?

# Lab 2

### Task 1: Design a NIOS II System

![nios_setup1](/images/nios_setup1.png)
![nios_setup2](/images/nios_setup2.png)

Understanding so far:

* `cpu` represents the NIOSII component. Aside from the obvious _clk_ and _reset_ connections, it has a `data_master` connection, used for communicating with various slaves. `irq` represents interrupt signals, which are sent by the `jtag_uart` component
* `jtag_uart` component is used for communication between the FPGA board and the connected device, using the UART protocol.
* button, switch, led and hex0-5 make up the periphiral I/O devices on the board.
* external connections are required to use this setup in other higher level schematics.
* `conduit` = one-to-one connection?
* `clk` is shown as a separate component because it represents the physical, oscillating crystal on board the FPGA?

> Not sure how the master/slave thing is working, might make more sense later. Is this a high-level SPI, with MOSI / MISO being defined implicitly?

#### Defining Pins:

![niospins](/images/niospins.png)

The code above is copied from the generated `nios_setup_inst.v` into the _top file_. Note that the actual pin connections are filled in manually here.

At this poing, NIOS compiles but produces several (171) warnings. A couple that repeat are:

```console
Warning (332060): Node: MAX10_CLK1_50 was determined to be a clock but was found without an associated clock assignment.
```
And
```console
Warning (13024): Output pins are stuck at VCC or GND
	Warning (13410): Pin "DRAM_ADDR[0]" is stuck at GND
	Warning (13410): Pin "DRAM_ADDR[1]" is stuck at GND
	... very many other pins that we are not using
```
which I believe we can ignore at this stage.

### Task 2: Program a NIOS II System

![helloworldcode](/images/helloworldcode.png)

> Insert explanation

Having programmed the FPGA with `DE10_LITE_Golden_Top.sof`, Built the project, and generated a BSP as per the instructions, we open an instance of the `nios2-terminal` using:

```bash
nios2-terminal
```
and in a _separate_ terminal window, run

```bash
nios2-download -g hello_sw.elf
```
Both from the `lab2/software/hello_sw` directory.

> insert better explanation: This monitors the JTAG UART interface i think?

![nioshelloworld](/images/nios2helloworld.png)

# Appendix
---

## Constantly expanding list of bug fixes because intel cannot write software but hey at least i don't have a mac

### Fix for NIOS II SBT not booting up in eclipse

There are two reasons for why the NIOS II link in quartus does not initially work. Firstly, the instructions in

```bash
<quartus_install_dir>/nios2eds/bin/README.txt
```

need to be followed to install the nios2 plugins. Following this, the `eclipse-nios2` script will boot a _very_ degenerate version of eclipse (see next point).

Secondly, and far less obviously, the version of `GTK` used for the `cpp` version of eclipse (as opposed to the java version installed by the `snap` package manager) is not the default. As a result, the following environmental variable needs to be exported in `.bashrc`:

```bash
export SWT_GTK3=0 eclipse
```

> full credit to Omar Alkhatib for spending a whole day finding this.

Following this, eclipse must be run from the executable in _nios2eds/bin/eclipse-nios2_. Creating symbolic link is recommended.

### Fix for Platform Designer (QSYS) not scaling for High DPI displays

Set the environmental variable:

```bash
export QSYS_FONTSIZE=28
```
>This is the only solution, as Platform Designer does not use GNOME, nor responds to any changes in java variables (despite clearly making use of jdk for many of it's subcomponents), such as:
>```bash
java -Dsun.java2d.uiScale=2.5 -Dswing.aatext=true -Dis.hidpi=true
>```
All had no effect.

### Fix for no template options in Eclipse Project Wizard

Can work around this by using the `nios` command shell. Begin by creating an instance of the shell:

```bash
~/intelFPGA/nios2eds$ ./nios2_command_shell.sh
```
By setting the font size in the console to the minimum and screengrabbing at the exact correct moment, I was able to catch all the arguments passed to create a template of the `hello_world_small` project.

```bash
 nios2-swexample-create --sopc-file=/home/nik/eie/ip/lab2/nios_setup.sopcinfo --type=hello_world_small --elf-name=hello_sw.elf --app-dir=software/hello_sw --bsp-dir=software/hello_sw_bsp
```
> The above should be run from the project directory, i.e. /eie/ip/lab2 in my case

```bash
./create-this-bsp --cpu-name cpu --no-make
```
> This is run from the lab2/software/hello_world_bsp directory that will have been created by the previous command. It's only contents will be the `create-this-bsp` shell script.

Also run

```bash
./create-this-app
```
from _lab2/software/hello_sw_ if for some reason the nios script didn't trigger it.

Finally import both the `hello_sw` and `hello_sw_bsp` into eclipse.

> Go File > Import > Import Nios II Software Project > (path to software/hello_sw), then again for the hello_sw_bsp folder.

### Fix for JTAG board not responding despite being shown as connected by `lsusb`

First, `udev` rules for usb-blasting on ubuntu 22.04 need to be changed to the following:

```bash
SUBSYSTEM=="usb", ATTRS{idVendor}=="09fb",
ATTRS{idProduct}=="6001", GROUP="plugdev", MODE="0666",
SYMLINK+="usbblaster"
```
> Credit to Omar Alkhatib for finding the above

and saved in the `udev` directory as `37-usbblaster.rules`

Following this, _in theory_ you should be able to

1. Unplug the JTAG board, and restart the udev rules:
```bash
sudo service udev restart
```
2. Kill all existing `jtagd` processes
```bash
killall jtagd
```

3. Plug the board back in and run:
```
jtagconfig
```
Which should identify the serial number of the Altera device. The `jtagconfig` command may cry about some "unable to connect to server" nonsense but as long as it finds the serial number this is ok.

HOWEVER this usually only works 1 out of 10 times, and I find the only 100% accurate fix as the following script, which will run the jtag command twice first, allowing it to timeout after 1 second:

```bash
#!/bin/bash

killall jtagd
timeout 1s jtagconfig # this will fail, cancelling it in 1 second

killall jtagd
timeout 1s jtagconfig # and again bc idek why

echo "Please disconnect board..."

while true
do
  if [ -z "$(lsusb | grep Altera)" ] # checking that there is no connection
  then
    break
  fi
done

echo "Restarting udev service..."

sudo service udev restart
sleep 1

echo "Please reconnect board..."

while [ -z "$(lsusb | grep Altera)" ]  # checks for connection present
do
  sleep 0.1s
done

echo "JTAG board found."

jtagconfig
```

And the board is correctly identified :)
