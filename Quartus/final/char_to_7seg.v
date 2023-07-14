module char_to_7seg (out,in);

input 	[6:0] 	in;
output 	[7:0] 	out;
reg 		[7:0] 	conversions [95:0];
wire		[7:0]		index;


initial begin
	conversions[0] = ~{7'h00}; /* (space) */
	conversions[1] = ~{7'h86}; /* ! */
	conversions[2] = ~{8'h22}; /* " */
	conversions[3] = ~{8'h7E}; /* # */
	conversions[4] = ~{8'h6D}; /* $ */
	conversions[5] = ~{8'hD2}; /* % */
	conversions[6] = ~{8'h46}; /* & */
	conversions[7] = ~{8'h20}; /* ' */
	conversions[8] = ~{8'h29}; /* ( */
	conversions[9] = ~{8'h0B}; /* ) */
	conversions[10] = ~{8'h21}; /* * */
	conversions[11] = ~{8'h70}; /* + */
	conversions[12] = ~{8'h10}; /* }; */
	conversions[13] = ~{8'h40}; /* - */
	conversions[14] = ~{8'h80}; /* . */
	conversions[15] = ~{8'h52}; /* / */
	conversions[16] = ~{8'h3F}; /* 0 */
	conversions[17] = ~{8'h06}; /* 1 */
	conversions[18] = ~{8'h5B}; /* 2 */
	conversions[19] = ~{8'h4F}; /* 3 */
	conversions[20] = ~{8'h66}; /* 4 */
	conversions[21] = ~{8'h6D}; /* 5 */
	conversions[22] = ~{8'h7D}; /* 6 */
	conversions[23] = ~{8'h07}; /* 7 */
	conversions[24] = ~{8'h7F}; /* 8 */
	conversions[25] = ~{8'h6F}; /* 9 */
	conversions[26] = ~{8'h09}; /* : */
	conversions[27] = ~{8'h0D}; /* ; */
	conversions[28] = ~{8'h61}; /* < */
	conversions[29] = ~{8'h48}; /* = */
	conversions[30] = ~{8'h43}; /* > */
	conversions[31] = ~{8'hD3}; /* ? */
	conversions[32] = ~{8'h5F}; /* @ */
	conversions[33] = ~{8'h77}; /* A */
	conversions[34] = ~{8'h7C}; /* B */
	conversions[35] = ~{8'h39}; /* C */
	conversions[36] = ~{8'h5E}; /* D */
	conversions[37] = ~{8'h79}; /* E */
	conversions[38] = ~{8'h71}; /* F */
	conversions[39] = ~{8'h3D}; /* G */
	conversions[40] = ~{8'h76}; /* H */
	conversions[41] = ~{8'h30}; /* I */
	conversions[42] = ~{8'h1E}; /* J */
	conversions[43] = ~{8'h75}; /* K */
	conversions[44] = ~{8'h38}; /* L */
	conversions[45] = ~{8'h15}; /* M */
	conversions[46] = ~{8'h37}; /* N */
	conversions[47] = ~{8'h3F}; /* O */
	conversions[48] = ~{8'h73}; /* P */
	conversions[49] = ~{8'h6B}; /* Q */
	conversions[50] = ~{8'h33}; /* R */
	conversions[51] = ~{8'h6D}; /* S */
	conversions[52] = ~{8'h78}; /* T */
	conversions[53] = ~{8'h3E}; /* U */
	conversions[54] = ~{8'h3E}; /* V */
	conversions[55] = ~{8'h2A}; /* W */
	conversions[56] = ~{8'h76}; /* X */
	conversions[57] = ~{8'h6E}; /* Y */
	conversions[58] = ~{8'h5B}; /* Z */
	conversions[59] = ~{8'h39}; /* [ */
	conversions[60] = ~{8'h64}; /* \ */
	conversions[61] = ~{8'h0F}; /* ] */
	conversions[62] = ~{8'h23}; /* ^ */
	conversions[63] = ~{8'h08}; /* _ */
	conversions[64] = ~{8'h02}; /* ` */
	conversions[65] = ~{8'h5F}; /* a */
	conversions[66] = ~{8'h7C}; /* b */
	conversions[67] = ~{8'h58}; /* c */
	conversions[68] = ~{8'h5E}; /* d */
	conversions[69] = ~{8'h7B}; /* e */
	conversions[70] = ~{8'h71}; /* f */
	conversions[71] = ~{8'h6F}; /* g */
	conversions[72] = ~{8'h74}; /* h */
	conversions[73] = ~{8'h10}; /* i */
	conversions[74] = ~{8'h0C}; /* j */
	conversions[75] = ~{8'h75}; /* k */
	conversions[76] = ~{8'h30}; /* l */
	conversions[77] = ~{8'h14}; /* m */
	conversions[78] = ~{8'h54}; /* n */
	conversions[79] = ~{8'h5C}; /* o */
	conversions[80] = ~{8'h73}; /* p */
	conversions[81] = ~{8'h67}; /* q */
	conversions[82] = ~{8'h50}; /* r */
	conversions[83] = ~{8'h6D}; /* s */
	conversions[84] = ~{8'h78}; /* t */
	conversions[85] = ~{8'h1C}; /* u */
	conversions[86] = ~{8'h1C}; /* v */
	conversions[87] = ~{8'h14}; /* w */
	conversions[88] = ~{8'h76}; /* x */
	conversions[89] = ~{8'h6E}; /* y */
	conversions[90] = ~{8'h5B}; /* z */
	conversions[91] = ~{8'h46}; /* { */
	conversions[92] = ~{8'h30}; /* | */
	conversions[93] = ~{8'h70}; /* } */
	conversions[94] = ~{8'h01}; /* ~ */
	conversions[95] = ~{8'h00}; /* (del) */
end

assign index = in - 32;
assign out = conversions[index];

endmodule
