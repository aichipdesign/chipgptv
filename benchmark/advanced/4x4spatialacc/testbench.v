module testbed();
reg clk;
reg rst;
reg [15:0] weight[0:3][0:3];
reg [15:0] inputt[0:15];
wire [31:0] outputt[0:15];
// Instantiate DUT
reference dut(
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
  // Inputs 
  clk = 1;
  #10
  rst <= 1;
  #10
  rst <= 0;
  #10
  weight[0][0] = 1; weight[0][1] = 2; weight[0][2] = 3; weight[0][3] = 4;
  weight[1][0] = 5; weight[1][1] = 6; weight[1][2] = 7; weight[1][3] = 8;
  weight[2][0] = 9; weight[2][1] = 10; weight[2][2] = 11; weight[2][3] = 12;
  weight[3][0] = 13; weight[3][1] = 14; weight[3][2] = 15; weight[3][3] = 16;

  inputt[0] = 1; inputt[1] = 2; inputt[2] = 3; inputt[3] = 4;
  inputt[4] = 5; inputt[5] = 6; inputt[6] = 7; inputt[7] = 8;
  inputt[8] = 9; inputt[9] = 10; inputt[10] = 11; inputt[11] = 12;
  inputt[12] = 13; inputt[13] = 14; inputt[14] = 15; inputt[15] = 16;
  // Run 1 cycle
  #10

  // Verify result
  if (outputt[0] != 1) $error("outputt[0] error: %0d", outputt[0]);
  if (outputt[1] != 4) $error("outputt[1] error: %0d", outputt[1]);
  if (outputt[2] != 9) $error("outputt[2] error: %0d", outputt[2]);
  if (outputt[3] != 16) $error("outputt[3] error: %0d", outputt[3]);
  if (outputt[4] != 25) $error("outputt[4] error: %0d", outputt[4]);
  if (outputt[5] != 36) $error("outputt[5] error: %0d", outputt[5]);
  if (outputt[6] != 49) $error("outputt[6] error: %0d", outputt[6]);
  if (outputt[7] != 64) $error("outputt[7] error: %0d", outputt[7]);
  if (outputt[8] != 81) $error("outputt[8] error: %0d", outputt[8]);
  if (outputt[9] != 100) $error("outputt[9] error: %0d", outputt[9]);
  if (outputt[10] != 121) $error("outputt[10] error: %0d", outputt[10]);
  if (outputt[11] != 144) $error("outputt[11] error: %0d", outputt[11]);
  if (outputt[12] != 169) $error("outputt[12] error: %0d", outputt[12]);
  if (outputt[13] != 196) $error("outputt[13] error: %0d", outputt[13]);
  if (outputt[14] != 225) $error("outputt[14] error: %0d", outputt[14]);
  if (outputt[15] != 256) $error("outputt[15] error: %0d", outputt[15]);

  #10
  if (outputt[0] != 2) $error("outputt[0] error: %0d", outputt[0]);
  if (outputt[1] != 8) $error("outputt[1] error: %0d", outputt[1]);
  if (outputt[2] != 18) $error("outputt[2] error: %0d", outputt[2]);
  if (outputt[3] != 32) $error("outputt[3] error: %0d", outputt[3]);
  if (outputt[4] != 50) $error("outputt[4] error: %0d", outputt[4]);
  if (outputt[5] != 72) $error("outputt[5] error: %0d", outputt[5]);
  if (outputt[6] != 98) $error("outputt[6] error: %0d", outputt[6]);
  if (outputt[7] != 128) $error("outputt[7] error: %0d", outputt[7]);
  if (outputt[8] != 162) $error("outputt[8] error: %0d", outputt[8]);
  if (outputt[9] != 200) $error("outputt[9] error: %0d", outputt[9]);
  if (outputt[10] != 242) $error("outputt[10] error: %0d", outputt[10]);
  if (outputt[11] != 288) $error("outputt[11] error: %0d", outputt[11]);
  if (outputt[12] != 338) $error("outputt[12] error: %0d", outputt[12]);
  if (outputt[13] != 392) $error("outputt[13] error: %0d", outputt[13]);
  if (outputt[14] != 450) $error("outputt[14] error: %0d", outputt[14]);
  if (outputt[15] != 512) $error("outputt[15] error: %0d", outputt[15]);
  // Finish test
  $display("===========Your Design passed===========")
  $finish;
end
initial begin
  $monitor("At %0t: output[0] = %0d, output[1] = %0d, output[2] = %0d, output[3] = %0d, output[4] = %0d, output[5] = %0d, output[6] = %0d, output[7] = %0d, output[8] = %0d, output[9] = %0d, output[10] = %0d, output[11] = %0d, output[12] = %0d, output[13] = %0d, output[14] = %0d, output[15] = %0d",
    $time, outputt[0], outputt[1], outputt[2], outputt[3], outputt[4], outputt[5], outputt[6], outputt[7], outputt[8], outputt[9], outputt[10], outputt[11], outputt[12], outputt[13], outputt[14], outputt[15]);

end

endmodule