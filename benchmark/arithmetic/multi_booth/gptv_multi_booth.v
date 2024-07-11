module booth4_mul #(
    parameter WIDTH_M = 8,  // Width of the multiplicand
    parameter WIDTH_R = 8   // Width of the multiplier
)(
    input clk,
    input rstn,
    input vld_in,
    input [WIDTH_M-1:0] multiplicand,
    input [WIDTH_R-1:0] multiplier,
    output reg [WIDTH_M+WIDTH_R-1:0] mul_out,
    output reg done
);

    // Define the partial product wires and Booth encodings
    wire [WIDTH_M:0] partial_products[3:0];
    wire [2:0] booth_encodings[1:0];

    // Booth Encoder / Selector for bits [0 1 2]...
    booth_encoder booth0 (
        .multiplier_bits({1'b0, multiplier[1:0]}), // Zero-padded
        .multiplicand(multiplicand),
        .partial_product(partial_products[0])
    );
    
    // ... Add the remaining Booth encoders here ...

    // 16-bit Carry Save Adders
    // Note: You would need to adjust the size of the adders based on the partial products
    // since the multiplicand width is parameterized.
    wire [15:0] sum0, sum1, sum2;
    wire [15:0] carry0, carry1, carry2;

    // ... Instantiate Carry Save Adders here ...

    // The final step would be a conventional adder to sum the results of the CSAs.
    // A simple CSA chain is shown here, but you will need to implement or instantiate
    // the CSAs and a final adder to add the sum and carry results.

    // Output assignment and done signal generation
    always @(posedge clk or negedge rstn) begin
        if (!rstn) begin
            mul_out <= 0;
            done <= 0;
        end else if (vld_in) begin
            // Assuming the final adder step is completed here
            // Assign the result to mul_out and assert done.
            done <= 1'b1;
        end else begin
            done <= 1'b0;
        end
    end

    // ... Rest of the implementation ...

endmodule

// Booth Encoder/Selector Module
module booth_encoder(
    input [2:0] multiplier_bits,
    input [WIDTH_M-1:0] multiplicand,
    output reg [WIDTH_M:0] partial_product
);
    // Booth encoding logic here

    // ... Booth encoding and partial product generation ...

endmodule

// Carry Save Adder Module (you would define your own CSA module)
module carry_save_adder(
    // Define your CSA ports and logic here
);
    // ... CSA implementation ...

endmodule
