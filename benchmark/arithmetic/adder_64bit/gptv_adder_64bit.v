`timescale 1ns / 1ps

module adder_64bit #(
    parameter DATA_WIDTH = 64
)(
    input clk,
    input rst_n,
    input i_en,
    input [DATA_WIDTH-1:0] adda,
    input [DATA_WIDTH-1:0] addb,
    output reg [DATA_WIDTH:0] result,
    output reg o_en
);

// Intermediate carry and sum signals
wire [3:0] carry[0:15];
wire [DATA_WIDTH-1:0] sum;

// Pipeline stage registers
reg [15:0] stage_carry[0:3]; // Pipeline registers for carry
reg [DATA_WIDTH-1:0] stage_sum[0:3];  // Pipeline registers for sum
reg stage_en[0:3]; // Pipeline registers for enable

// 4-bit adders instantiation
genvar i;
generate
    for (i = 0; i < DATA_WIDTH/4; i = i+1) begin : adders
        // First stage adders have a carry-in of 0
        if (i == 0) begin
            assign carry[i] = {3'b0, i_en};
        end else begin
            assign carry[i] = stage_carry[2][i-1];
        end

        // Instantiate a 4-bit adder; for simplicity, we use the built-in addition operator
        assign {carry[i+1][0], sum[i*4 +: 4]} = adda[i*4 +: 4] + addb[i*4 +: 4] + carry[i][0];
    end
endgenerate

// Pipeline logic
integer j;
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        // Reset all pipeline registers
        for (j = 0; j < 4; j = j+1) begin
            stage_carry[j] <= 0;
            stage_sum[j] <= 0;
            stage_en[j] <= 0;
        end
        result <= 0;
        o_en <= 0;
    end else begin
        // Pipeline stage 0
        stage_sum[0] <= sum;
        stage_carry[0] <= carry[DATA_WIDTH/4];
        stage_en[0] <= i_en;

        // Pipeline stages 1 to 3
        for (j = 1; j < 4; j = j+1) begin
            stage_sum[j] <= stage_sum[j-1];
            stage_carry[j] <= stage_carry[j-1];
            stage_en[j] <= stage_en[j-1];
        end

        // Set output
        result <= {stage_carry[3][15], stage_sum[3]};
        o_en <= stage_en[3];
    end
end

endmodule
