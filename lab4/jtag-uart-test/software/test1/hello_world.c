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

#include <stdio.h>
#include <string.h>

int main()
{
	printf("Running..\n");
	FILE* fp;
	char prompt = 0;
	// create file pointer to jtag_uart port
	fp = fopen ("/dev/jtag_uart", "r+");

	if (fp) {
		// here 'v' is used as the character to stop the program
		while (prompt != 'v') {
			// accept the character that has been sent down
			prompt = getc(fp);
			if (prompt != 'v') {
				// using the '<-->' characters to indicate to the python host
				//     program when the output string starts and ends
				// the 0x4 character is used the send ^D up to the host side
				//     nios2-terminal so that it exits and the python program
				//     can continue
				fprintf(fp, "<--> Detected the character %c. <--> \n", prompt);
			}
			if (ferror(fp)) {
				clearerr(fp);
			}
		}
		fprintf(fp, "Closing the JTAG UART file handle.\n %c",0x4);
		fclose(fp);
	}
	printf("Complete\n");

	return 0;
}