module reference (
  input clk,
  input rst,
  input [15:0] a0,
  input [15:0] a1,
  input [15:0] b0,
  output [31:0] c0,
  output [31:0] c1
);
  reg [15:0] b1;
  PE pe0 (
    .clk(clk),
    .rst(rst),
    .a(a0),
    .b(b0),
    .c(c0)
  );
  PE pe1 (
    .clk(clk),
    .rst(rst),
    .a(a1),
    .b(b1),
    .c(c1)
  );
  always@(posedge clk or posedge rst) begin
    if(rst) begin
      b1 <= 0;
    end
    else begin
      b1 <= b0; // pass b0 to next PE
    end
  end
  
endmodule