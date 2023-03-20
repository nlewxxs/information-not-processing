//------------------------------
// Module name: ex3_top
// Function: Top level module for part 1 ex3
//   				to dispaly 10 switch setting on 3 7-seg displays
// Creator:  Peter Cheung
// Version:  2.0
// Date:     22 Oct 2016
//------------------------------
module seg_display (
		INPUT,					// input 16-bit number		
		HEX0, HEX1, HEX2, HEX3, HEX4, HEX5	// Hex output on 7 segment display									
	 );
	input		[23:0]	INPUT;		// declare input/output ports			
	output	[7:0]		HEX0, HEX1, HEX2, HEX3, HEX4, HEX5;
	wire 		[15:0]	bcd;

	bin2bcd BIN2BCD (INPUT[13:0], bcd);

	hex_to_7seg		SEG0 (HEX0, bcd[3:0]);			
	hex_to_7seg		SEG1 (HEX1, bcd[7:4]);			
	hex_to_7seg		SEG2 (HEX2, bcd[11:8]);
	hex_to_7seg		SEG3 (HEX3, bcd[15:12]);
	hex_to_7seg		SEG4 (HEX4, INPUT[19:16]);
	hex_to_7seg		SEG5 (HEX5, INPUT[23:20]);

endmodule
