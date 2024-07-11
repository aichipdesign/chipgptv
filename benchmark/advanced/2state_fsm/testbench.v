module tb_state_machine();
// Inputs 
reg a = 0;
reg b = 0;
reg clk = 1;
reg rst = 0;
// Outputs
wire [3:0] state;
// Instantiate DUT 
state_machine dut (
  .a(a),
  .b(b),
  .clk(clk),
  .rst(rst),
  .state(state)
);
// Clock generation
always #5 clk = ~clk; 
initial begin
  // Initialize inputs
  rst = 1;
  #20 rst = 0;
  // Apply input sequence
  #10; a = 1; b = 0;
  #10; a = 1; b = 0;
  #10; a = 1; b = 0;
  // Verify outputs
  if (state != 4'b1001) begin
    $display("ERROR: Incorrect state transition");
    $display("This is a test number: %b.", state);
  end
  else
    $display("Your design pass!!!");
  $finish;
end
endmodule