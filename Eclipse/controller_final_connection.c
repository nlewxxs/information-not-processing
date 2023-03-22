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
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "alt_types.h"
#include <sys/alt_stdio.h>

#define THRESHOLD_1G 255 //Threshold for 1G (force of gravity)
#define INACT_SAMPLES 1000

alt_32 yz[] = {0,0}; //array of readings for each axis
int act_thresh_coef[2][2] = {{15,14},
							 {15,15}};
int inact_thresh_coef[2] = {2,2};
char output[2][2] = {{'U','D'},   //force downward is positive,
					 {'L','R'} }; //force left is positive
char char_out = '0';

alt_u8 led = 0x1; //global LED counter to show interrupts occurring
int en_f = 1;
int timer_f = 0;
int inact_counter = 0;
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
	led++;
	IOWR_ALTERA_AVALON_PIO_DATA(LED_BASE, led);
	timer_f = 1;
}

void read_accelerometer(alt_32* yz) {
	//readings for all axes
	alt_up_accelerometer_spi_read_y_axis(acc_dev, yz);
	alt_up_accelerometer_spi_read_z_axis(acc_dev, yz+1);
}

int max() { //returns index of the maximum reading out of the 3 axes (current sample)
	int index = 0;
	int max = abs(yz[0]);
	for (int i=1; i<2; i++) {
		if (abs(yz[i]) > max) {
			max = abs(yz[i]);
			index = i;
		}
	}
	return index;
}

int min() { //returns index of the maximum reading out of the 3 axes (current sample)
	int index = 0;
	int min = abs(yz[0]);
	for (int i=1; i<2; i++) {
		if (abs(yz[i]) < min) {
			min = abs(yz[i]);
			index = i;
		}
	}
	return index;
}

int detect_ACT() {
	int i = max();

	//output char if the |acceleration|>threshold and gradient has same polarity
	if (yz[i]*10 > (act_thresh_coef[i][0]*THRESHOLD_1G)) { //multiplied by 10 to fine-tune threshold
		char_out = output[i][0];
		led++;
		return 1;
	} else if ((yz[i]*10 < -(act_thresh_coef[i][1]*THRESHOLD_1G))) { //Threshold cannot be below 255 as tilting the controller can cause reading abs(255) in any axis
		char_out = output[i][1];
		led++;
		return 1;
	} else {
		char_out = '0';
		return 0; //return 0 if reading magnitude too small
	}
}

int detect_INACT(int i){
	if ((abs(yz[i])*10) < (inact_thresh_coef[i]*THRESHOLD_1G)) { //multiplied by 10 to fine-tune threshold
		return 1;
	} else {
		return 0; //return 0 if reading magnitude too large
	}
}

int wait_INACT() {
	int i = min();
	if (inact_counter < INACT_SAMPLES) {
		if (detect_INACT(i)) {
			inact_counter++;
		} else {
			inact_counter = 0;
		}
		return 0;
	} else {
		inact_counter = 0;
		return 1;
	}

}

//input should be 2 characters and a 16 bit score (30bits overall)
void write_7seg(char* characters, alt_16 score) {
	alt_u32 format_char0 = ((alt_u32)(characters[0]) << 25) >> 2;
	alt_u32 format_char1 = ((alt_u32)(characters[1]) << 25) >> 9;
	alt_u32 output = format_char0 + format_char1 + abs(score);
	printf("%d %c\n", output >> 23, output >> 23);
	IOWR_ALTERA_AVALON_PIO_DATA(HEX_DISPLAY_BASE, output);
}

int main(){

	acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
	if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
		return 1;
	}
	alt_up_accelerometer_spi_write(acc_dev, 0x1F, -63);
	//By default accelerometer reads 1g,0g
	//writing to Y OFFSET register on accelerometer, accounting for 1g caused by gravity.
	//The offset is scaled by a factor of 2 so (127 - 2*-63=0)(127=1G according to datasheet)
	//The output is scaled to 8 bits (255=1G), difference is confusing but worked.

	printf("connected\n");

	//TEST HEX DISPLAY
	char characters[2] = {'S','c'};
	printf("%d\n",'s'); //s has ASCII value of 115, S has ASCII value of 83
	alt_16 score = 123;
	write_7seg(characters, score);

	printf("start");

	//INITIALIZING ISR
	timer_init(sys_timer_isr);

	printf("end");

	while(1){

		//READ DATA
		alt_32 yz_raw[] = {0,0};
		read_accelerometer(yz_raw);

		//FILTER DATA
		IOWR_ALTERA_AVALON_PIO_DATA(FILTER_Y_IN_BASE, yz_raw[0]);
		IOWR_ALTERA_AVALON_PIO_DATA(FILTER_Z_IN_BASE, yz_raw[1]);

		yz[0] = IORD_ALTERA_AVALON_PIO_DATA(FILTER_Y_OUT_BASE);
		yz[1] = IORD_ALTERA_AVALON_PIO_DATA(FILTER_Z_OUT_BASE);

		//PROCESS INPUT
		if (en_f) {
			en_f = !detect_ACT();
		} else if (!en_f) {
			en_f = wait_INACT();
		}

		//OUTPUT
		if (timer_f) {
			printf("%c\n", char_out);
			timer_f = 0;
		}



	}

	return 0;
}
