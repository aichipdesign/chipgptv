`timescale 1ns/1ns

module testbench;

  // Inputs
  reg clk;
  reg rst_n;
  reg valid_a;
  reg data_a;

  // Outputs
  wire ready_a;
  wire valid_b;
  wire [5:0] data_b;

  // Instantiate the module to be tested
  s_to_p dut (
    .clk(clk),
    .rst_n(rst_n),
    .valid_a(valid_a),
    .data_a(data_a),
    .ready_a(ready_a),
    .valid_b(valid_b),
    .data_b(data_b)
  );

  // Clock generation
  always #5 clk = ~clk;

  // Initial block
  integer error = 0;
  initial begin
    clk = 0;
    rst_n = 0;
    valid_a = 0;
    data_a = 0;

    // Reset for a few clock cycles
    #50; 
    rst_n = 1;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #20;
    valid_a = 1;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #10;
    valid_a = 0;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #10;
    valid_a = 1;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #20;
    data_a = 1;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #10;
    valid_a = 0;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #30;
    valid_a = 1;
    data_a = 0;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #10;
    data_a = 1;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #10;
    valid_a = 0;
    $display("ready_a is %b, valid_b is %b",ready_a,valid_b,ready_a);
    #20;
    valid_a = 1;
    $display("data_b is %b, valid_b is %b, ready_a is %b",data_b,valid_b,ready_a);
    error = (data_b == 6'b101000) ? error : error+1;

	  $display("error is %d",error);

    if(error==0) begin
      $display("===========Your Design Passed===========");
      $display("error is %d",error);
    end
    else begin
      $display("===========Error===========");
    end
    $finish; // End the simulation
  end

endmodule

