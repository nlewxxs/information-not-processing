module clock_divider (clk, rst, clk_div);

input wire clk;
input wire rst;
output reg clk_div;

reg [31:0] count;
localparam constNumber = 25000;

always @ (posedge(clk), posedge(rst))
begin
    if (rst == 1'b1)
        count <= 32'b0;
    else if (count == constNumber - 1)
        count <= 32'b0;
    else
        count <= count + 1;
end

always @ (posedge(clk), posedge(rst))
begin
    if (rst == 1'b1)
        clk_div <= 1'b0;
    else if (count == constNumber - 1)
        clk_div <= ~clk_div;
    else
        clk_div <= clk_div;
end

endmodule
