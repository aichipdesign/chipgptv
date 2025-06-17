module testbed();
// Inputs 
reg clk;
reg rst;
reg [15:0] a0 = 0;
reg [15:0] a1 = 0;
reg [15:0] a2 = 0;
reg [15:0] a3 = 0;
reg [15:0] b0 = 0;
// Outputs
wire [31:0] c0, c1, c2, c3;
// Instantiate 4 PE module
systolic1x4 dut (
  .clk(clk),
  .rst(rst),
  .a0(a0),
  .a1(a1),
  .a2(a2),
  .a3(a3),
  .b0(b0),
  .c0(c0),
  .c1(c1),
  .c2(c2),
  .c3(c3)
);
// Clock generation
always #5 clk = ~clk; 
// Stimulus
initial begin
  clk = 1;
  #10;
  rst <= 1;
  #10;
  rst <= 0;
  #10;
  a0 = 5; b0 = 5; a1 = 5; a2 = 5; a3 = 5;

  #10;
  a0 = 10; b0 = 10;
  if (c0 != 25)
    $error("Error: c0=%d", c0);
  if (c1 != 0)
    $error("Error: c1=%d", c1);
  if (c2 != 0)
    $error("Error: c2=%d", c2);
  if (c3 != 0)
    $error("Error: c3=%d", c3);
  #10;
  a0 = 20; b0 = 20;
  if (c0 != 125)
    $error("Error: c0=%d", c0);
  if (c1 != 25)
    $error("Error: c1=%d", c1);
  if (c2 != 0)
    $error("Error: c2=%d", c2);
  if (c3 != 0)
    $error("Error: c3=%d", c3);
  #10;
  if (c0 != 525)
    $error("Error: c0=%d", c0);
  if (c1 != 75)
    $error("Error: c1=%d", c1);
  if (c2 != 25)
    $error("Error: c2=%d", c2);
  if (c3 != 0)
    $error("Error: c3=%d", c3);
  $display("===========Your Design passed===========");
  $finish;
end
// Monitor outputs 
initial begin
  $monitor("Time=%0t a0=%0d b0=%0d | c0=%0d c1=%0d c2=%0d c3=%0d",
    $time, a0, b0, c0, c1, c2, c3);
end
endmodule