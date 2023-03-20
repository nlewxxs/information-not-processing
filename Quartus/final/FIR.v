module fir_lp (clk, in, out);

input 									clk;
input signed				[31:0]	in;
output signed				[31:0]	out;

reg signed 	[31:0]		mem 		[15:0];
reg signed  [31:0]		h 			[15:0];
wire signed [63:0]		t 			[15:0];
wire signed [63:0]		intermediate;

//initial begin
//	h[0] = 32'h3f9e9026; //The decimal value is left-shifted by 32 bits, equivalent to *2^(32)
//	h[1] = 32'h3fae4922; //We assume the maximum value of each coefficient is 0.99999 
//	h[2] = 32'hbfafd3b7; //Meaning that max val is 2^32
//	h[3] = 32'h3f948376; // So the max sum 
//	h[4] = 32'h3fb05d01;
//	h[5] = 32'hbfbd3a62;
//	h[6] = 32'h3f9107c8;
//	h[7] = 32'h3fe158fe;
//	h[8] = 32'h3fe158fe;
//	h[9] = 32'h3f9107c8;
//	h[10] = 32'hbfbd3a62;
//	h[11] = 32'h3fb05d01;
//	h[12] = 32'h3f948376;
//	h[13] = 32'hbfafd3b7;
//	h[14] = 32'h3fae4922;
//	h[15] = 32'h3f9e9026;
//end

//cut-off frequency 10
initial begin
	h[0] = 32'h3f864390;
	h[1] = 32'hbfb2fd07;
	h[2] = 32'hbfaac61c;
	h[3] = 32'hbf9a4234;
	h[4] = 32'h3fa0e0d9;
	h[5] = 32'h3fbd57dd;
	h[6] = 32'h3fc8ddd3;
	h[7] = 32'h3fcf27c0;
	h[8] = 32'h3fcf27c0;
	h[9] = 32'h3fc8ddd3;
	h[10] = 32'h3fbd57dd;
	h[11] = 32'h3fa0e0d9;
	h[12] = 32'hbf9a4234;
	h[13] = 32'hbfaac61c;
	h[14] = 32'hbfb2fd07;
	h[15] = 32'h3f864390;
end

always @ (posedge clk) begin
	mem[15] <= mem[14];
	mem[14] <= mem[13];
	mem[13] <= mem[12];
	mem[12] <= mem[11];
	mem[11] <= mem[10];
	mem[10] <= mem[9];
	mem[9] <= mem[8];
	mem[8] <= mem[7];
	mem[7] <= mem[6];
	mem[6] <= mem[5];
	mem[5] <= mem[4];
	mem[4] <= mem[3];
	mem[3] <= mem[2];
	mem[2] <= mem[1];
	mem[1] <= mem[0];
	mem[0] <= in;
end
	
assign t[0] = mem[0] * h[0]; 
assign t[1] = mem[1] * h[1];
assign t[2] = mem[2] * h[2];
assign t[3] = mem[3] * h[3];
assign t[4] = mem[4] * h[4];
assign t[5] = mem[5] * h[5];
assign t[6] = mem[6] * h[6];
assign t[7] = mem[7] * h[7];
assign t[8] = mem[8] * h[8];
assign t[9] = mem[9] * h[9];
assign t[10] = mem[10] * h[10];
assign t[11] = mem[11] * h[11];
assign t[12] = mem[12] * h[12];
assign t[13] = mem[13] * h[13];
assign t[14] = mem[14] * h[14];
assign t[15] = mem[15] * h[15];

assign intermediate = t[0]+t[1]+t[2]+t[3]+t[4]+t[5]+t[6]+t[7]+t[8]+t[9]+t[10]+t[11]+t[12]+t[13]+t[14]+t[15];

assign out = intermediate[63:32];

endmodule
