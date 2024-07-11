module multi_16bit(
    input clk,      
    input rst_n,      
    input start,      
    input [15:0] ain, 
    input [15:0] bin,
    output reg [31:0] yout,
    output reg done
);

// Internal signals
reg [15:0] multiplicand;
reg [15:0] multiplier;
reg [31:0] product;
reg [4:0] count; // 5-bit counter for 16 cycles

// Shift add multiplier process
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        multiplicand <= 16'b0;
        multiplier <= 16'b0;
        product <= 32'b0;
        count <= 5'b0;
        done <= 1'b0;
    end else if (start) begin
        multiplicand <= ain;
        multiplier <= bin;
        product <= 32'b0;
        count <= 5'b0;
        done <= 1'b0;
    end else if (count < 16) begin
        if (multiplier[0]) // If LSB of multiplier is 1
            product <= product + (multiplicand << count);
        multiplier <= multiplier >> 1; // Shift right multiplier
        count <= count + 1;
    end else begin
        done <= 1'b1; // Assert done when count reaches 16
    end
end

// Output assignment
always @(posedge clk) begin
    if (done)
        yout <= product;
end

endmodule
