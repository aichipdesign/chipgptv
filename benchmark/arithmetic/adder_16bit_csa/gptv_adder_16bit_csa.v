module full_adder(input a, input b, input cin, output sum, output cout);
    assign sum = a ^ b ^ cin;
    assign cout = (a & b) | (cin & (a ^ b));
endmodule

module mux_2to1(input a, input b, input sel, output y);
    assign y = (sel) ? b : a;
endmodule

module carry_select_adder_16bit(input [15:0] a, input [15:0] b, input cin, output [15:0] sum, output cout);
    wire [3:0] s0_0, s0_1, s1_0, s1_1, co_0, co_1, s[3:0];
    wire co0, co1, co2, co3;

    // Full adders when carry-in is '0'
    full_adder fa0_0(a[0], b[0], 0, s0_0, co_0[0]);
    full_adder fa1_0(a[1], b[1], co_0[0], s0_1, co_0[1]);
    full_adder fa2_0(a[2], b[2], co_0[1], s1_0, co_0[2]);
    full_adder fa3_0(a[3], b[3], co_0[2], s1_1, co_0[3]);

    // Full adders when carry-in is '1'
    full_adder fa0_1(a[0], b[0], 1, s0_0, co_1[0]);
    full_adder fa1_1(a[1], b[1], co_1[0], s0_1, co_1[1]);
    full_adder fa2_1(a[2], b[2], co_1[1], s1_0, co_1[2]);
    full_adder fa3_1(a[3], b[3], co_1[2], s1_1, co_1[3]);

    // Muxes to select the outputs
    mux_2to1 m0(co_0[0], co_1[0], cin, co0);
    mux_2to1 m1(co_0[1], co_1[1], cin, co1);
    mux_2to1 m2(co_0[2], co_1[2], cin, co2);
    mux_2to1 m3(co_0[3], co_1[3], cin, co3);

    mux_2to1 m_s0(s0_0, s0_1, cin, s[0]);
    mux_2to1 m_s1(s0_1, s1_0, cin, s[1]);
    mux_2to1 m_s2(s1_0, s1_1, cin, s[2]);
    mux_2to1 m_s3(s1_1, co_1[3], cin, s[3]);

    assign sum = {s[3], s[2], s[1], s[0], a[15:4] + b[15:4] + co3};
    assign cout = co3;

endmodule
