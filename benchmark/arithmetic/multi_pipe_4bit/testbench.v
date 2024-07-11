`timescale 1ns/1ns

module multi_pipe_tb;

    // Parameters
    parameter size = 4;
    parameter N = size * 2;

    // Testbench Signals
    reg clk;
    reg rst_n;
    reg [size-1:0] mul_a;
    reg [size-1:0] mul_b;
    wire [N-1:0] mul_out;

    // Instantiate the Unit Under Test (UUT)
    multi_pipe #(size) uut (
        .clk(clk),
        .rst_n(rst_n),
        .mul_a(mul_a),
        .mul_b(mul_b),
        .mul_out(mul_out)
    );

    // Clock Generation
    initial begin
        clk = 0;
        forever #5 clk = ~clk; // Generate a clock with 10ns period
    end

    // Test Stimulus
    initial begin
        // Reset
        rst_n = 0;
        mul_a = 0;
        mul_b = 0;
        #20; // Wait for a few clock cycles after reset
        rst_n = 1; // Release reset

        // Test case 1
        #20; // Wait for a few clock cycles
        mul_a = 4'b0011;
        mul_b = 4'b0101;
        #500; // Wait for the result to propagate
        checkResult(mul_a * mul_b, mul_out);

        // Test case 2
        #20;
        mul_a = 4'b1100;
        mul_b = 4'b0110;
        #500; // Wait for the result to propagate
        checkResult(mul_a * mul_b, mul_out);

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
        $monitor("Time = %d, mul_a = %b, mul_b = %b, mul_out = %b", $time, mul_a, mul_b, mul_out);
    end

endmodule
