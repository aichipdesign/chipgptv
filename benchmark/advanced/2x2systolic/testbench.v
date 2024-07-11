module tb_systolic_array();
// Inputs
reg clk;
reg rst;
reg [15:0] weight[0:1][0:1];
reg [15:0] inputt[0:1][0:1];
// Outputs
wire [31:0] outputt[0:1][0:1];
// Instantiate systolic array
systolic2x2 dut (
  .clk(clk),
  .rst(rst),
  .weight(weight),
  .inputt(inputt),
  .outputt(outputt)
);
// Clock generation
always #5 clk = ~clk;
// Stimulus
initial begin
  clk = 1;
  rst <= 1;
  #10
  rst <= 0;
  #10
  weight[0][0] = 1; weight[0][1] = 2;
  weight[1][0] = 3; weight[1][1] = 4;
  inputt[0][0] = 10; inputt[0][1] = 20;
  inputt[1][0] = 5; inputt[1][1] = 10;
  #10
  if (outputt[0][0] != 10) $error("outputt[0][0] error: %0d", outputt[0][0]);
  if (outputt[0][1] != 40) $error("outputt[0][1] error: %0d", outputt[0][1]);
  if (outputt[1][0] != 15) $error("outputt[1][0] error: %0d", outputt[1][0]);
  if (outputt[1][1] != 40) $error("outputt[1][1] error: %0d", outputt[1][1]);
  #10
  if (outputt[0][0] != 20) $error("outputt[0][0] error: %0d", outputt[0][0]);
  if (outputt[0][1] != 80) $error("outputt[0][1] error: %0d", outputt[0][1]);
  if (outputt[1][0] != 30) $error("outputt[1][0] error: %0d", outputt[1][0]);
  if (outputt[1][1] != 80) $error("outputt[1][1] error: %0d", outputt[1][1]);
  $display("===========Your Design passed===========")
  $finish;
end
// Monitor outputs
initial begin
  $monitor("At %0t: output[0][0]=%0d output[0][1]=%0d output[1][0]=%0d output[1][1]=%0d",
    $time, outputt[0][0], outputt[0][1], outputt[1][0], outputt[1][1],);
end
endmodule