// Code your testbench here
// or browse Examples
`timescale 1ns/1ns
module testbed;

  reg clk;
  reg rst;
  reg [15:0] a;
  reg [15:0] b;

  wire [31:0] c;

  PE pe (
    .clk(clk),
    .rst(rst),
    .a(a),
    .b(b),
    .c(c)
  );

  always #5 clk = ~clk;

  initial begin
    clk = 1;
    rst <= 1;
    #10 rst <= 0;
    a = 10; b = 20;
    #10
    #10 a = 30; b = 40;
    if (c != 200)
        $error("Error: c=%d", c);
    #10 if (c != 1400)
        $error("Error: c=%d", c);
    $display("Your design passed!!!");
    $finish;
  end
   // Monitoring
  initial begin
    $monitor("At %t: a0=%0d b0=%0d | c0=%0d",
      $time, a, b, c);
  end

endmodule