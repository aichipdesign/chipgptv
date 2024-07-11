module pulse_detect(
    input clk_fast,
    input clk_slow,
    input rst_n,
    input data_in,
    output reg data_out
);

// Intermediate signals for synchronization
reg data_level;
reg data_level1_reg, data_level2_reg;
reg data_level3_reg;

// Detecting the rising edge of the pulse in the fast clock domain
always @(posedge clk_fast or negedge rst_n) begin
    if (!rst_n) begin
        data_level <= 1'b0;
    end else begin
        if (data_in && !data_level)
            data_level <= 1'b1; // Capture the rising edge
        else
            data_level <= 1'b0; // Reset after one clock cycle
    end
end

// Synchronizing the detected pulse to the slow clock domain
always @(posedge clk_slow or negedge rst_n) begin
    if (!rst_n) begin
        data_level1_reg <= 1'b0;
        data_level2_reg <= 1'b0;
        data_level3_reg <= 1'b0;
    end else begin
        data_level1_reg <= data_level; // First stage of synchronization
        data_level2_reg <= data_level1_reg; // Second stage
        data_level3_reg <= data_level2_reg; // Third stage
    end
end

// Generating the single clock-width pulse in the slow clock domain
always @(posedge clk_slow or negedge rst_n) begin
    if (!rst_n) begin
        data_out <= 1'b0;
    end else begin
        // Create a pulse when data_level3_reg goes high and wasn't high the previous cycle
        data_out <= data_level3_reg && !data_level2_reg;
    end
end

endmodule
