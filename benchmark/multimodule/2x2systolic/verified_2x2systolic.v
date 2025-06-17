
module reference(
  input clk,
  input rst,
  input [15:0] weight [0:1] [0:1], // weight station
  input [15:0] inputt [0:1] [0:1],        // input buffer
  output [31:0] outputt [0:1] [0:1]      // output buffer 
);
// PE instances
PE pe00(.clk(clk), .rst(rst), .a(inputt[0][0]), .b(weight[0][0]), .c(outputt[0][0]));
PE pe01(.clk(clk), .rst(rst), .a(inputt[0][1]), .b(weight[0][1]), .c(outputt[0][1]));
PE pe10(.clk(clk), .rst(rst), .a(inputt[1][0]), .b(weight[1][0]), .c(outputt[1][0]));
PE pe11(.clk(clk), .rst(rst), .a(inputt[1][1]), .b(weight[1][1]), .c(outputt[1][1]));
endmodule

module PE (
  input clk,
  input rst,
  input [15:0] a,
  input [15:0] b,
  output[31:0] c
);
  reg [31:0] r;
  always @(posedge clk or posedge rst) begin
    if (rst)
      r <= 0;
    else
      r <= r + (a * b);
  end
  assign c = r;
endmodule