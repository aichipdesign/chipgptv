module div_16bit(
    input wire [15:0] A,  // Dividend
    input wire [15:0] B,  // Divisor
    output reg [15:0] result,  // Quotient
    output reg [15:0] remainder  // Remainder
);

    // Internal signals
    reg [15:0] dividend;
    reg [31:0] temp_dividend;
    reg [15:0] divisor;
    reg [15:0] temp_remainder;
    integer i;

    always @(A or B) begin
        // Initial assignments
        dividend = A;
        divisor = B;
        temp_dividend = {16'd0, dividend};  // Zero-extend dividend to 32 bits
        temp_remainder = 0;
        result = 0; // Clear quotient

        // Division algorithm
        for (i = 15; i >= 0; i = i - 1) begin
            // Shift left temp_remainder and bring down the next bit from the dividend
            temp_remainder = temp_remainder << 1;
            temp_remainder[0] = temp_dividend[31];
            temp_dividend = temp_dividend << 1;  // Shift left dividend

            // Compare and subtract
            if (temp_remainder >= divisor) begin
                temp_remainder = temp_remainder - divisor;
                result[i] = 1;  // Set quotient bit
            end
        end

        // Final remainder
        remainder = temp_remainder;
    end

endmodule
