// Code your testbench here
// or browse Examples
module tb_chained_pe;
  // Inputs
  reg clk;
  reg rst;
  reg [15:0] a0;
  reg [15:0] a1;
  reg [15:0] b0;
  // Outputs 
  wire [31:0] c0;
  wire [31:0] c1;
  // Unit Under Test
  nocpe1x2 uut (
    .clk(clk),
    .rst(rst),
    .a0(a0),
    .a1(a1),
    .b0(b0),
    .c0(c0),
    .c1(c1) 
  );
  // Clock generation
  always #5 clk = ~clk;
  // Stimulus
  initial begin
    clk = 1;
    a0 = 5; b0 = 10; a1 = 5;
    #10;
    rst <= 1;
    #10;
    rst <= 0;
    #20;
    if(c0 != 50) $error("c0 error: %0d", c0);
    a0 = 20; b0 = 15;
    #10;
    if(c0 != 350) $error("c0 error: %0d", c0);
    if(c1 != 50) $error("c1 error: %0d", c1);
    $display("Your design passed!!!");
    $finish;
  end
  // Monitoring
  initial begin
    $monitor("At %t: a0=%0d b0=%0d | c0=%0d c1=%0d",
      $time, a0, b0, c0, c1);
  end
endmodule