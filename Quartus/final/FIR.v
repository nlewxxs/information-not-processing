module fir_lp (clk, in, out);

input 									clk;
input signed				[31:0]	in;
output signed				[31:0]	out;

reg signed 	[31:0]		mem 		[31:0];
reg signed  [31:0]		h 			[31:0];
wire signed	[63:0]		t			[31:0];
wire signed  [63:0] intermediate;


//cut-off frequency 100
initial begin
	h[0] = 32'h3f8dd709;
	h[1] = 32'h3f692f90;
	h[2] = 32'hbf366aad;
	h[3] = 32'hbf7977c8;
	h[4] = 32'hbf8ba4c9;
	h[5] = 32'hbf94d07c;
	h[6] = 32'hbf98e621;
	h[7] = 32'hbf979171;
	h[8] = 32'hbf8db49c;
	h[9] = 32'h3f60f369;
	h[10] = 32'h3f9abb65;
	h[11] = 32'h3fac62c7;
	h[12] = 32'h3fb62a39;
	h[13] = 32'h3fbd82bc;
	h[14] = 32'h3fc19371;
	h[15] = 32'h3fc31b68;
	h[16] = 32'h3fc31b68;
	h[17] = 32'h3fc19371;
	h[18] = 32'h3fbd82bc;
	h[19] = 32'h3fb62a39;
	h[20] = 32'h3fac62c7;
	h[21] = 32'h3f9abb65;
	h[22] = 32'h3f60f369;
	h[23] = 32'hbf8db49c;
	h[24] = 32'hbf979171;
	h[25] = 32'hbf98e621;
	h[26] = 32'hbf94d07c;
	h[27] = 32'hbf8ba4c9;
	h[28] = 32'hbf7977c8;
	h[29] = 32'hbf366aad;
	h[30] = 32'h3f692f90;
	h[31] = 32'h3f8dd709;
end

always @ (posedge clk) begin
	integer i;
	for (i = 31; i>0; i=i-1) begin
		mem[i] <= mem[i-1];
	end
	mem[0] <= in;
end

assign t[0] = mem[0]*h[0];
assign t[1] = mem[1]*h[1];
assign t[2] = mem[2]*h[2];
assign t[3] = mem[3]*h[3];
assign t[4] = mem[4]*h[4];
assign t[5] = mem[5]*h[5];
assign t[6] = mem[6]*h[6];
assign t[7] = mem[7]*h[7];
assign t[8] = mem[8]*h[8];
assign t[9] = mem[9]*h[9];
assign t[10] = mem[10]*h[10];
assign t[11] = mem[11]*h[11];
assign t[12] = mem[12]*h[12];
assign t[13] = mem[13]*h[13];
assign t[14] = mem[14]*h[14];
assign t[15] = mem[15]*h[15];
assign t[16] = mem[16]*h[16];
assign t[17] = mem[17]*h[17];
assign t[18] = mem[18]*h[18];
assign t[19] = mem[19]*h[19];
assign t[20] = mem[20]*h[20];
assign t[21] = mem[21]*h[21];
assign t[22] = mem[22]*h[22];
assign t[23] = mem[23]*h[23];
assign t[24] = mem[24]*h[24];
assign t[25] = mem[25]*h[25];
assign t[26] = mem[26]*h[26];
assign t[27] = mem[27]*h[27];
assign t[28] = mem[28]*h[28];
assign t[29] = mem[29]*h[29];
assign t[30] = mem[30]*h[30];
assign t[31] = mem[31]*h[31];


assign intermediate = t[0]+t[1]+t[2]+t[3]+t[4]+t[5]+t[6]+t[7]+t[8]+t[9]+t[10]+t[11]+t[12]+t[13]+t[14]+t[15]+t[16]+t[17]+t[18]+t[19]+t[20]+t[21]+t[22]+t[23]+t[24]+t[25]+t[26]+t[27]+t[28]+t[29]+t[30]+t[31];

assign out = intermediate[63:32];

endmodule
