/* action_detection-transient code used to detect a strong movement in a direction aligned with 3D axes.
 * A sharp movement is characterised by an acceleration in the positive direction and then an acceleration in the negative direction (deceleration)
 * A small routine is used to wait for the acceleration transient of an arm movement becomes bounded by a selected threshold
 * After the transient is negligible, input is enabled again.*/

//accelerometer SPI HAL: https://people.ece.cornell.edu/land/courses/ece5760/DE1_SOC/Accelerometer_SPI_Mode.pdf
//accelerometer datasheet: https://www.analog.com/media/en/technical-documentation/data-sheets/adxl345.pdf
//NIOSII interrupts: https://www.intel.com/content/dam/support/us/en/programmable/support-resources/fpga-wiki/asset03/appendixd-using-interrupt-service-routines.pdf
//NIOSII timer doc: https://pages.mtu.edu/~saeid/multimedia/labs/Documentation/n2cpu_nii51008_Interval_Timer.pdf
//altera timer: http://www-ug.eecg.toronto.edu/msl/nios_devices/datasheets/Altera%20Timer.pdf
//ISRs: http://www-ug.eecg.toronto.edu/desl/manuals/n2sw_nii52006.pdf

#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>
#include <stdio.h>

#define DISPLAY_BASE 0x41040
#define THRESHOLD_1G 255 //Threshold for 1G (force of gravity)

alt_u8 led = 0x1; //global LED counter to show interrupts occurring
alt_32 xyz[] = {0,0,0}; //array of readings for each axis
int act_thresh_coef[3][2] = {	{12,12},
								{13,11},
								{11,13}};
int inact_thresh_coef[3] = {2,2,2};
char output[3][2] = {	{'F','B'}, //force left is positive
						{'U','D'}, //force forward is positive
						{'L','R'} }; //force downward is positive,

int f=0; //flag for isr
int nox = 0; //flag to exclude F/B from detection
alt_up_accelerometer_spi_dev * acc_dev;

//Timer is used to regulate the maximum rate of data input to the game.
void timer_init(void * isr) { //initialises timer and specifies interrupt service routine
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0000); //change period of timer with these two registers
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0008); // PERIOD = {PERIODH,PERIODL} (concatenated)
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);
}

void sys_timer_isr() { //interrupt service routine
	IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
	f = 1;

	IOWR(LED_BASE, 0, led);
	IOWR(DISPLAY_BASE, 0, led);
	led++;
}

void read_accelerometer() {
	//readings for all axes
	alt_up_accelerometer_spi_read_x_axis(acc_dev, xyz);
	alt_up_accelerometer_spi_read_y_axis(acc_dev, xyz+1);
	alt_up_accelerometer_spi_read_z_axis(acc_dev, xyz+2);
}

int max() { //returns index of the maximum reading out of the 3 axes (current sample)
	int max = abs(xyz[nox]);
	int index = nox;
	for (int i=1; i<3; i++) {
		if (abs(xyz[i]) > max) {
			max = abs(xyz[i]);
			index = i;
		}
	}
	return index;
}

int min() { //returns index of the maximum reading out of the 3 axes (current sample)
	int min = abs(xyz[nox]);
	int index = nox;
	for (int i=1; i<3; i++) {
		if (abs(xyz[i]) < min) {
			min = abs(xyz[i]);
			index = i;
		}
	}
	return index;
}

int detect(int i) { //outputs char when input reading's magnitude is above threshold
	if (xyz[i]*10 > (act_thresh_coef[i][0]*THRESHOLD_1G)) { //multiplied by 10 to fine-tune threshold
		putchar(output[i][0]);
		return 1;
	} else if (xyz[i]*10 < -(act_thresh_coef[i][1]*THRESHOLD_1G)) { //Threshold cannot be below 255 as tilting the controller can cause reading abs(255) in any axis
		putchar(output[i][1]);
		return 1;
	} else {
		putchar('0');
		return 0; //return 0 if reading magnitude too small
	}
}

int detect_INACT(int i){
	if ((abs(xyz[i])*10) < (inact_thresh_coef[i]*THRESHOLD_1G)) { //multiplied by 10 to fine-tune threshold
		return 1;
	} else {
		return 0; //return 0 if reading magnitude too large
	}
}

void process_action() { //selects the axis with largest reading and checks if above threshold
	int flag;
	int i = max();
	flag = detect(i);
	printf("\n");
	if (flag == 1) {
		//This snippet of code waits for the transient of arm movement to settle
		//It waits until 1000 consecutive, "inactive" readings are received.
		//inactive threshold is tunable to each direction and axis.
		int inact_counter = 0;
		while (inact_counter < 1000) {
			read_accelerometer();
			i = min();
			if (detect_INACT(i)) {
				inact_counter++;
			} else inact_counter = 0;
			//printf("xyz[%d]: %ld\tinact_counter: %d\n", i, xyz[i], inact_counter);
		}
	}
}

int main(){

	acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
	if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
		return 1;
	}
	alt_up_accelerometer_spi_write(acc_dev, 0x1F, -63);
	//By default accelerometer reads 0g,0g,1g
	//writing to Z OFFSET register on accelerometer, accounting for 1g caused by gravity.
	//The offset is scaled by a factor of 2 so (127 - 2*-63=0)(127=1G according to datasheet)
	//The output is scaled to 8 bits (255=1G), difference is confusing but worked.

	nox = 1;

	timer_init(sys_timer_isr); //initialising timer with isr

	while(1){
		read_accelerometer();
		//isr triggers flag. Standard C I/O operations not allowed in isr, must be done in the main
		if (f) {
			//printf("%ld,%ld,%ld\n",xyz[0],xyz[1],xyz[2]);
			//printf("max reading: %d\n",max());
			process_action();
			f = 0;
		}
	}

	return 0;
}
