module JC_counter(
    input clk,
    input rst_n,  // Active low reset
    output reg [63:0] Q
);

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // Synchronous reset on falling edge of rst_n
        Q <= 64'b0;
    end else begin
        // Shift left the current value of Q
        Q <= {Q[62:0], ~Q[63]};
    end
end

endmodule
