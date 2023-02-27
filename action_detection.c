/* action_detection code used to detect a strong movement in a direction aligned with 3D axes.
 * A sharp movement is characterised by an acceleration in the positive direction and then an acceleration in the negative direction (deceleration)
 * At the moment, we are outputting both the acceleration and deceleration, hope to only output the first acceleration
 * Could be implemented with a second timer which disables output in a short window after initial acceleration is detected*/

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

#define THRESHOLD_1G 255 //Threshold for 1G (force of gravity)

alt_u8 led = 0x1; //global LED counter to show interrupts occurring
alt_32 xyz[] = {0,0,0}; //array of readings for each axis
const char output[3][2] = {	{'R','L'}, //force left is positive
							{'F','B'}, //force forward is positive
							{'D','U'} }; //force downward is positive,

int f=0; //flag for isr

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
	IOWR(LED_BASE, 0, led);
	led++;
	f = !f;
}

int detect(alt_32* _read, char pos, char neg) { //outputs char when input reading's magnitude is above threshold
	if ((*_read)*10 > 15*THRESHOLD_1G) { //multiplied by 10 to fine-tune threshold
		putchar(pos);
		return 1;
	} else if ((*_read)*10 < -15*THRESHOLD_1G) { //Threshold cannot be below 255 as tilting the controller can cause reading abs(255) in any axis
		putchar(neg);
		return 1;
	} else {
		return 0; //return 0 if reading magnitude too small
	}
}

//Old function, will output all readings that go above the threshold
void detect_xyz() {
	int flag = 0;
	for (int i=0; i<3; i++) {
		flag += detect(xyz+i, output[i][0], output[i][1]);
	}
	if (flag > 0) {
		printf("\n");
	} else {
		//printf("IDLE\n");
	}
}

int max() { //returns index of the maximum reading out of the 3 axes (current sample)
	int max = abs(xyz[0]);
	int index = 0;
	for (int i=1; i<3; i++) {
		if (abs(xyz[i]) > max) {
			max = abs(xyz[i]);
			index = i;
		}
	}
	return index;
}

void detect_action() { //selects the axis with largest reading and checks if above threshold
	int flag;
	int i = max();
	flag = detect(xyz+i, output[i][0], output[i][1]);
	if (flag == 1) printf("\n");//newline if an output was produced
}

int main(){

	alt_up_accelerometer_spi_dev * acc_dev;
	acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
	if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
		return 1;
	}

	alt_up_accelerometer_spi_write(acc_dev, 0x20, -63);
	//By default accelerometer reads 0g,0g,1g
	//writing to Z OFFSET register on accelerometer, accounting for 1g caused by gravity.
	//The offset is scaled by a factor of 2 so (127 - 2*-63=0)(127=1G according to datasheet)
	//The output is scaled to 8 bits (255=1G), difference is confusing but worked.

	timer_init(sys_timer_isr); //initialising timer with isr

	while(1){

		//readings for all axes
		alt_up_accelerometer_spi_read_x_axis(acc_dev, xyz);
		alt_up_accelerometer_spi_read_y_axis(acc_dev, xyz+1);
		alt_up_accelerometer_spi_read_z_axis(acc_dev, xyz+2);

		//isr triggers flag. Standard C I/O operations not allowed in isr, must be done in the main
		if (f == 1) {
			//printf("%ld,%ld,%ld\n",xyz[0],xyz[1],xyz[2]);
			//printf("max reading: %d\n",max());
			detect_action();
			f = !f;
		}
	}

	return 0;
}
