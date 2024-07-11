`timescale 1ns / 1ps

module right_shifter_tb;

reg clk;
reg d;
wire [7:0] q;

right_shifter dut (
    .clk(clk),
    .d(d),
    .q(q)
);


always #10 clk = ~clk;

initial begin
    // Initialize inputs
    clk = 0;
    d = 0;
    
    // Apply inputs and observe outputs
    #5 d = 1;
    #5 
    if (q !== 8'b00000001) $error("Test failed for d=1");
    d = 0;
    #5 
    if (q !== 8'b00000010) $error("Test failed for d=0");
    d = 1;
    #5 
    if (q !== 8'b00000101) $error("Test failed for d=1");
    d = 1;
    #5 
    if (q !== 8'b00001011) $error("Test failed for d=1");
    d = 0;
    #5 
    if (q !== 8'b00010110) $error("Test failed for d=0");
    $display("All tests passed");
    $finish;
end



endmodule