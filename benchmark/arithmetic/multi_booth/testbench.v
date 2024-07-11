`timescale 1ns / 1ps

module booth4_mul_tb;

    // Parameters
    parameter WIDTH_M = 8;
    parameter WIDTH_R = 8;
    parameter N = WIDTH_M + WIDTH_R;

    // Testbench Signals
    reg clk;
    reg rstn;
    reg vld_in;
    reg [WIDTH_M-1:0] multiplicand;
    reg [WIDTH_R-1:0] multiplier;
    wire [N-1:0] mul_out;
    wire done;

    // Instantiate the Unit Under Test (UUT)
    booth4_mul #(WIDTH_M, WIDTH_R) uut (
        .clk(clk),
        .rstn(rstn),
        .vld_in(vld_in),
        .multiplicand(multiplicand),
        .multiplier(multiplier),
        .mul_out(mul_out),
        .done(done)
    );

    // Clock Generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // 100MHz Clock
    end

    // Test Stimulus
    initial begin
        // Reset
        rstn = 0;
        vld_in = 0;
        multiplicand = 0;
        multiplier = 0;
        #10;
        rstn = 1; // Release reset

        // Test Case 1
        #20;
        multiplicand = 8'h12; // Example inputs
        multiplier = 8'h34;
        vld_in = 1; // Start the operation
        #300; // Wait for the result to propagate
        checkResult(multiplicand * multiplier, mul_out);

        // Test Case 2
        #20;
        vld_in = 0; // Reset valid in
        multiplicand = 8'hAB;
        multiplier = 8'hCD;
        vld_in = 1; // Start the operation
        #300; // Wait for the result to propagate
        checkResult(multiplicand * multiplier, mul_out);

        // Add additional test cases as needed

        #100;
        $finish; // End simulation
    end

    // Task for checking results
    task checkResult;
        input [N-1:0] expected;
        input [N-1:0] actual;
        begin
            if (actual !== expected) begin
                $display("ERROR at time %d: Expected = %b, Actual = %b", $time, expected, actual);
            end
            else begin
                $display("Test passed at time %d: Expected = %b, Actual = %b", $time, expected, actual);
            end
        end
    endtask

    // Monitor
    initial begin
        $monitor("Time = %d, vld_in = %b, multiplicand = %h, multiplier = %h, mul_out = %h, done = %b", $time, vld_in, multiplicand, multiplier, mul_out, done);
    end

endmodule
