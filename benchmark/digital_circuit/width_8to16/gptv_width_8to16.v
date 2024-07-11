module width_8to16(
    input clk,
    input rst_n,
    input valid_in,
    input [7:0] data_in,
    output reg valid_out,
    output reg [15:0] data_out
);

// Internal signal declaration
reg [7:0] high_byte;
reg [7:0] low_byte;
reg valid_in_delayed;

// State Machine for input handling
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        high_byte <= 0;
        low_byte <= 0;
        valid_in_delayed <= 0;
        valid_out <= 0;
        data_out <= 0;
    end else begin
        // Delay the valid_in signal for proper data alignment
        valid_in_delayed <= valid_in;
        
        if (valid_in) begin
            // First byte - store it in the high byte of the output
            high_byte <= data_in;
        end else if (valid_in_delayed) begin
            // Second byte - store it in the low byte of the output and update the output
            low_byte <= data_in;
            valid_out <= 1;
            data_out <= {high_byte, low_byte};
        end else begin
            // Reset valid_out when there is no input valid
            valid_out <= 0;
        end
    end
end

endmodule
