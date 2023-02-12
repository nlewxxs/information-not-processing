/*
 * "Hello World" example.
 *
 * This example prints 'Hello from Nios II' to the STDOUT stream. It runs on
 * the Nios II 'standard', 'full_featured', 'fast', and 'low_cost' example
 * designs. It runs with or without the MicroC/OS-II RTOS and requires a STDOUT
 * device in your system's hardware.
 * The memory footprint of this hosted application is ~69 kbytes by default
 * using the standard reference design.
 *
 * For a reduced footprint version of this template, and an explanation of how
 * to reduce the memory footprint for a given application, see the
 * "small_hello_world" template.
 *
 */
#include <string.h>
#include "system.h"
#include "altera_up_avalon_accelerometer_spi.h"
#include "altera_avalon_timer_regs.h"
#include "altera_avalon_timer.h"
#include "altera_avalon_pio_regs.h"
#include "sys/alt_irq.h"
#include <stdlib.h>
#include <float.h>
#include <math.h>
#include <stdio.h>
#include <sys/alt_stdio.h>
#include <sys/alt_timestamp.h>

#define OFFSET -32
#define PWM_PERIOD 16
#define ALT_TIMESTAMP_CLK TIMER

alt_8 pwm = 0;
alt_u8 led;
int level;

void led_write(alt_u8 led_pattern) {
    IOWR(LED_BASE, 0, led_pattern);
}

void convert_read(alt_32 acc_read, int * level, alt_u8 * led) {
    acc_read += OFFSET;
    alt_u8 val = (acc_read >> 6) & 0x07;
    * led = (8 >> val) | (8 << (8 - val));
    * level = (acc_read >> 1) & 0x1f;
}

void sys_timer_isr() {
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);

    if (pwm < abs(level)) {

        if (level < 0) {
            led_write(led << 1);
        } else {
            led_write(led >> 1);
        }

    } else {
        led_write(led);
    }

    if (pwm > PWM_PERIOD) {
        pwm = 0;
    } else {
        pwm++;
    }

}

void timer_init(void * isr) {

    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0003);
    IOWR_ALTERA_AVALON_TIMER_STATUS(TIMER_BASE, 0);
    IOWR_ALTERA_AVALON_TIMER_PERIODL(TIMER_BASE, 0x0900);
    IOWR_ALTERA_AVALON_TIMER_PERIODH(TIMER_BASE, 0x0000);
    alt_irq_register(TIMER_IRQ, 0, isr);
    IOWR_ALTERA_AVALON_TIMER_CONTROL(TIMER_BASE, 0x0007);

}


alt_32 fir(float coeffs[], alt_32 raw_data[], int n){
	// N-TAP FIR filter
	float y = 0;

	for (; n > 0; n--){ // runs n times for
		// alt_printf("n value: %x\n", (alt_32)(n-1));
		// this print command makes it run smoother??
		y += coeffs[n-1]*(float)raw_data[n-1];
	}

	return (alt_32)y; // cast back to alt_32
}

alt_32 fir_quantized(alt_32 coeffs[], alt_32 raw_data[], int n){
	// N-TAP quantized FIR filter
	alt_32 y = 0;

	for (; n > 0; n--){ // runs n times for
//		alt_printf("Rounded coeff: %x\n", coeffs[n-1]);
		y += coeffs[n-1]*raw_data[n-1];
	}

	return round(y/100000); // converting back to appropriate value for LEDs
}

int main() {

	float matlab_coeffs[] = {0.00464135470656760, 	0.00737747226463043,
			-0.00240768675012549,	-0.00711018685736960,
			0.00326564674118811,	6.11463173516297e-05,
			-0.00935761974859676,	0.00397493281996669,
			0.00437887161977042,	-0.0133160721439149,
			0.00304771783859210,	0.0114361953193935,
			-0.0179286984033957,	-0.00107408161324030,
			0.0222597890359562,		-0.0224772654507762,
			-0.0108744542661829,	0.0395972756447093,
			-0.0263221720611839,	-0.0337570326573828,
			0.0751987217099385,		-0.0288978194901786,
			-0.120354853218164,		0.287921968939103,
			0.636863388360281,		0.287921968939103,
			-0.120354853218164,		-0.0288978194901786,
			0.0751987217099385,		-0.0337570326573828,
			-0.0263221720611839,	0.0395972756447093,
			-0.0108744542661829,	-0.0224772654507762,
			0.0222597890359562,		-0.00107408161324030,
			-0.0179286984033957,	0.0114361953193935,
			0.00304771783859210, 	-0.0133160721439149,
			0.00437887161977042,	0.00397493281996669,
			-0.00935761974859676,	6.11463173516297e-05,
			0.00326564674118811, 	-0.00711018685736960,
			-0.00240768675012549,	0.00737747226463043,
			0.00464135470656760};

	int n = 49; 	// len of coeff array
	// init coeffs from matlab
	float *fir_coeffs = calloc((n+1), sizeof(float)); // init a 49-tap filter, leave space for null pointer
	for (int coeff = 0; coeff < n; coeff++){
		fir_coeffs[coeff] = matlab_coeffs[coeff]; // populating
	}


    alt_32 x_read[n]; 									// raw data array
    alt_32 y; 											// filtered output

    alt_32 int_coeffs[n];
    for(int j = 0; j < n; j++){
    	int_coeffs[j] = (alt_32)round(fir_coeffs[j]*100000); // populate quantized coeffs
    	// multiplying by 10^m to grab m of the decimal places
    }

    FILE* fp;
    alt_8 mode = 0; // mode 0 = unfiltered, mode 1 = filtered.
    char prompt = 0;
    fp = fopen ("/dev/jtag_uart", "r+");

    alt_up_accelerometer_spi_dev * acc_dev;
    acc_dev = alt_up_accelerometer_spi_open_dev("/dev/accelerometer_spi");
    if (acc_dev == NULL) { // if return 1, check if the spi ip name is "accelerometer_spi"
        return 1;
    }

    timer_init(sys_timer_isr);

    while(1) {

    	for(alt_u8 j = 0; j < 200; j++){
    		// shift register
			for (int i = 0; i < n; i++){
				x_read[i+1] = x_read[i];
			}

			// update accel value
			alt_up_accelerometer_spi_read_x_axis(acc_dev, & x_read[0]);
			// filter output

			if (mode == 1) {

				y = fir_quantized(int_coeffs, x_read, n);
				alt_printf("y value (filtered): %x\n", y);

			} else if (mode == 0) {

				y = x_read[0];
				alt_printf("y value (raw): %x\n", y);
			}

			convert_read(y, & level, & led);
    	}

    	if (fp) {
    		prompt = getc(fp);
    		fprintf(fp, "<--> Detected the character %c <--> \n", prompt);
    		if (prompt == '1') {
    			mode = 1;
    		} else if (prompt == '0') {
    			mode = 0;
    		} else if (prompt == 'c') {

    			alt_printf("BOARD: preparing for coefficient update\n");

    			char *buffer = calloc(30, sizeof(char));
    			float *new_coeffs = calloc(49, sizeof(char));
    			buffer[29] = '\0'; // set a null pointer

    			int coeff_count = 0; // counts number of coeffs
    			int character_count = 0;

    			prompt = getc(fp); // reads from jtag_uart interface

    			while (prompt != 'x'){
    				fflush(stdout);
    				alt_printf("BOARD << received: %c \n", prompt);
    				fflush(stdout);

    				if (prompt == ','){

    					new_coeffs[coeff_count] = atof(buffer);
    					for(; character_count > 0; character_count--){
    						buffer[character_count] = '\0'; // two in one: clears buffer, and resets char count to 0
    					}
    					coeff_count++;

    				} else {

						buffer[character_count] = prompt;
						character_count++;
    				}

    				prompt = getc(fp);
    			}

    			fprintf(fp, "<UPDATED_COEFFICIENTS> %f\n", new_coeffs[0]);
    			fprintf(fp, "<UPDATED_COEFFICIENTS> %f\n", new_coeffs[1]);
    			fprintf(fp, "<UPDATED_COEFFICIENTS> %f\n", new_coeffs[2]);
    			fprintf(fp, "<UPDATED_COEFFICIENTS> %f\n", new_coeffs[3]);
    			fprintf(fp, "<UPDATED_COEFFICIENTS> %f\n", new_coeffs[4]);
    			fprintf(fp, "...\n");
    			fprintf(fp, "<UPDATED_COEFFICIENTS> %f\n", new_coeffs[49]);

    			for(int newc = 0; newc < 50; newc++){
    				fir_coeffs[newc] = new_coeffs[newc];
    				int_coeffs[newc] = (alt_32)round(new_coeffs[newc]*100000);
    			}

    			free(buffer);
    			free(new_coeffs);
    			buffer=NULL;
    			new_coeffs=NULL;

    		}

    	}
    }


    return 0;
}
