module s_to_p (
    input wire clk,
    input wire rst_n,
    input wire valid_a,
    input wire data_a,
    output reg ready_a,
    output reg valid_b,
    output reg [5:0] data_b
);

    // Internal signal declaration
    reg [2:0] count;  // 3-bit counter to count up to 6
    reg [5:0] shift_reg;  // Shift register to hold the incoming bits

    // Counter logic
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            count <= 3'd0;
        end else if (ready_a && valid_a) begin
            if (count == 3'd5) begin
                count <= 3'd0;  // Reset the counter after 6 bits are received
            end else begin
                count <= count + 1'b1;
            end
        end
    end

    // Control logic for ready_a and valid_b signals
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            ready_a <= 1'b0;
            valid_b <= 1'b0;
        end else begin
            ready_a <= (count < 3'd5);  // Ready to receive more bits until 6 bits are received
            valid_b <= (count == 3'd5) && valid_a;  // Output is valid when 6 bits are received
        end
    end

    // Shift register to store incoming bits
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            shift_reg <= 6'b0;
        end else if (ready_a && valid_a) begin
            shift_reg <= {shift_reg[4:0], data_a};  // Shift in the new bit at the lowest position
        end
    end

    // Assign the concatenated data to data_b when valid
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            data_b <= 6'b0;
        end else if (valid_b) begin
            data_b <= shift_reg;
        end
    end

endmodule
