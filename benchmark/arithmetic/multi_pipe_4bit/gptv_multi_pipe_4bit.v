module multi_pipe(
    input clk,
    input rst_n,
    input [3:0] mul_a,
    input [3:0] mul_b,
    output reg [7:0] mul_out
);

// Define intermediate pipeline registers
reg [3:0] stage1_temp1;
reg [3:0] stage1_temp2;
reg [3:0] stage1_temp3;
reg [3:0] stage1_temp4;

reg [7:0] stage2_sum1;
reg [7:0] stage2_sum2;

// Stage 1: Shift generation
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        stage1_temp1 <= 4'b0;
        stage1_temp2 <= 4'b0;
        stage1_temp3 <= 4'b0;
        stage1_temp4 <= 4'b0;
    end else begin
        stage1_temp1 <= mul_a & {4{mul_b[0]}};
        stage1_temp2 <= (mul_a & {4{mul_b[1]}}) << 1;
        stage1_temp3 <= (mul_a & {4{mul_b[2]}}) << 2;
        stage1_temp4 <= (mul_a & {4{mul_b[3]}}) << 3;
    end
end

// Stage 2: Addition
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        stage2_sum1 <= 8'b0;
        stage2_sum2 <= 8'b0;
    end else begin
        stage2_sum1 <= {4'b0, stage1_temp1} + {stage1_temp2, 4'b0};
        stage2_sum2 <= {stage1_temp3, 4'b0} + {stage1_temp4, 4'b0};
    end
end

// Stage 3: Final addition
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        mul_out <= 8'b0;
    end else begin
        mul_out <= stage2_sum1 + stage2_sum2;
    end
end

endmodule
