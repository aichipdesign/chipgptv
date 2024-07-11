module multi_pipe_8bit #(parameter size = 8) (
    input clk,          
    input rst_n, 
    input mul_en_in,      
    input [size-1:0] mul_a,       
    input [size-1:0] mul_b,  	
    output reg mul_en_out,  
    output reg [size*2-1:0] mul_out
);

// Internal signal declaration
reg [size-1:0] shift_gen_a, shift_gen_b;
reg [size-1:0] temp_0, temp_1, temp_2, temp_3, temp_4, temp_5, temp_6, temp_7;
reg [size*2-1:0] adder1_out, adder2_out, adder3_out, adder4_out, adder3_input1, adder3_input2;

// Shift generator
always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        shift_gen_a <= 0;
        shift_gen_b <= 0;
    end else if (mul_en_in) begin
        shift_gen_a <= mul_a;
        shift_gen_b <= mul_b;
    end
end

// Compute partial products
always @(posedge clk) begin
    temp_0 <= shift_gen_a & {size{shift_gen_b[0]}};
    temp_1 <= shift_gen_a & {size{shift_gen_b[1]}};
    temp_2 <= shift_gen_a & {size{shift_gen_b[2]}};
    temp_3 <= shift_gen_a & {size{shift_gen_b[3]}};
    temp_4 <= shift_gen_a & {size{shift_gen_b[4]}};
    temp_5 <= shift_gen_a & {size{shift_gen_b[5]}};
    temp_6 <= shift_gen_a & {size{shift_gen_b[6]}};
    temp_7 <= shift_gen_a & {size{shift_gen_b[7]}};
end

// Adder stages
always @(posedge clk) begin
    adder1_out <= {temp_1, size{1'b0}} + {temp_0, 1'b0};
    adder2_out <= {temp_3, size{1'b0}} + {temp_2, 1'b0};
    adder3_input1 <= {temp_5, size{1'b0}} + {temp_4, 1'b0};
    adder4_out <= {temp_7, size{1'b0}} + {temp_6, 1'b0};
end

// Second stage of adders
always @(posedge clk) begin
    adder3_input2 <= adder4_out;
    adder3_out <= adder3_input1 + (adder3_input2 << size/2);
end

// Final adder and output assignment
always @(posedge clk) begin
    if (!rst_n) begin
        mul_en_out <= 0;
        mul_out <= 0;
    end else begin
        mul_out <= adder1_out + (adder2_out << size) + (adder3_out << size/2);
        mul_en_out <= mul_en_in; // Pipeline the enable signal as well
    end
end

endmodule
