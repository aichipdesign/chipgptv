module adder_16bit (
    input [15:0] a,
    input [15:0] b,
    input c_up,
    output [15:0] y,
    output Co
);

// Using previously defined adder_8bit
wire intermediate_carry;
wire [7:0] lower_sum, upper_sum;

adder_8bit lower_adder (
    .a(a[7:0]),
    .b(b[7:0]),
    .cin(c_up),
    .sum(lower_sum),
    .SUM(intermediate_carry),
    .cout(intermediate_carry)  // This will act as cin for the upper adder
);

adder_8bit upper_adder (
    .a(a[15:8]),
    .b(b[15:8]),
    .cin(intermediate_carry),
    .sum(upper_sum),
    .SUM(Co),
    .cout(Co)  // The final carry out
);

// Combining the 8-bit results to form 16-bit output
assign y = {upper_sum, lower_sum};

endmodule
