`timescale 1ns/1ns

module testbench;

  // Inputs
  reg clk;
  reg rst;
  reg [3:0] d;
  
  // Outputs
  wire valid_in;
  wire dout;
  

  // Instantiate the module to be tested
  p_to_s dut (
    .clk(clk),
    .rst(rst),
    .d(d),
    .valid_in(valid_in),
    .dout(dout)
  );

  // Clock generation
  always #5 clk = ~clk;

  // Initial block
  integer error = 0;
  initial begin
    clk = 0;
    rst = 0;
    d = 0;
    

    // Reset for a few clock cycles
    #10 
    rst =0;
    #50
    rst =1;
    #20 
    d = 4'b1010;
    #30
    d = 4'b1111;
    #50
    d=4'b0010;
		$finish;
end

endmodule

