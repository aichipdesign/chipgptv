module edge_detect (
    input clk,
    input rst_n,
    input a,
    output reg rise,
    output reg down
);

// Register to hold the previous value of 'a'
reg a0;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // Asynchronous reset (active low)
        a0 <= 1'b0;
        rise <= 1'b0;
        down <= 1'b0;
    end
    else begin
        // Detect rising edge
        rise <= (a == 1'b1) && (a0 == 1'b0);

        // Detect falling edge
        down <= (a == 1'b0) && (a0 == 1'b1);

        // Update previous value of 'a'
        a0 <= a;
    end
end

endmodule
