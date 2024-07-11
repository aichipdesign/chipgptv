module adder_8bit (
    input [7:0] a, b,
    input cin,
    output [7:0] sum,
    output SUM,
    output cout
);

wire [7:0] carry;

// Define full adder using gates
module full_adder (a, b, cin, sum, cout);
    input a, b, cin;
    output sum, cout;
    
    wire a_xor_b, a_and_b, a_xor_b_and_cin;

    xor (a_xor_b, a, b);
    and (a_and_b, a, b);
    xor (sum, a_xor_b, cin);
    and (a_xor_b_and_cin, a_xor_b, cin);
    or (cout, a_and_b, a_xor_b_and_cin);
endmodule

// Instantiate 8 1-bit full adders
full_adder FA0(a[0], b[0], cin, sum[0], carry[0]);
full_adder FA1(a[1], b[1], carry[0], sum[1], carry[1]);
full_adder FA2(a[2], b[2], carry[1], sum[2], carry[2]);
full_adder FA3(a[3], b[3], carry[2], sum[3], carry[3]);
full_adder FA4(a[4], b[4], carry[3], sum[4], carry[4]);
full_adder FA5(a[5], b[5], carry[4], sum[5], carry[5]);
full_adder FA6(a[6], b[6], carry[5], sum[6], carry[6]);
full_adder FA7(a[7], b[7], carry[6], sum[7], carry[7]);

// Define cout and SUM
assign cout = carry[7];
or (SUM, cout, sum[7]);

endmodule
