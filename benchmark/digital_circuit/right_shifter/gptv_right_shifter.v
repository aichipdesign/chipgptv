module right_shifter (
    input clk,
    input d,
    output reg [7:0] q
);

    // On every positive edge of the clock
    always @(posedge clk) begin
        // Shift the register to the right
        q <= {d, q[7:1]};
    end

endmodule
