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