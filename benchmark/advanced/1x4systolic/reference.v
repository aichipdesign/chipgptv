module systolic1x4(
  input clk,
  input rst,
  input [15:0] a0,
  input [15:0] a1,
  input [15:0] a2,
  input [15:0] a3,
  input [15:0] b0,
  output [31:0] c0,
  output [31:0] c1,
  output [31:0] c2,
  output [31:0] c3 
);
reg [15:0] b1, b2, b3;
// 4 PEs
PE pe0(.clk(clk), .rst(rst), .a(a0), .b(b0), .c(c0));
PE pe1(.clk(clk), .rst(rst), .a(a1), .b(b1), .c(c1));
PE pe2(.clk(clk), .rst(rst), .a(a2), .b(b2), .c(c2));
PE pe3(.clk(clk), .rst(rst), .a(a3), .b(b3), .c(c3));
// Cascade b connections 
always@(posedge clk or posedge rst) begin
  if (rst) begin
    b1 <= 0;
    b2 <= 0;
    b3 <= 0;
  end
  else begin
    b1 <= b0; // pass b0 to next PE
    b2 <= b1;
    b3 <= b2;
  end
end
endmodule