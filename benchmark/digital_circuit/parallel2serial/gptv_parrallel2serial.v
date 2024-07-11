module p_to_s(
    input        clk,
    input        rst_n,
    input  [3:0] d,
    output       valid_in,
    output       dout
);

// Internal signal declarations
reg [3:0] shift_reg;
reg [1:0] counter;
wire      mux_sel;

// Counter logic for generating `valid_in` and `mux_sel` signal
assign valid_in = (counter == 3'b011); // When counter is 3, valid_in is high
assign mux_sel = counter;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        counter <= 2'b00;
        shift_reg <= 4'b0000;
    end else begin
        if (counter == 2'b11) begin
            counter <= 2'b00; // Reset the counter after 4 clock cycles
        end else begin
            counter <= counter + 2'b01; // Increment counter
        end
        shift_reg <= d; // Load new data on every new valid set
    end
end

// Parallel to serial conversion logic using shift register
assign dout = shift_reg[mux_sel];

endmodule
