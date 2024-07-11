module adder_32bit(
    input [31:0] A,
    input [31:0] B,
    output [31:0] S,
    output C32
);

    wire [3:0] g, p; // Generate and propagate signals for each 4-bit CLA block
    wire [3:0] c;    // Carry out from each 4-bit CLA block

    // Instantiate the 4-bit CLA adders
    cla_4bit cla0(.A(A[3:0]), .B(B[3:0]), .Ci(1'b0), .S(S[3:0]), .G(g[0]), .P(p[0]), .Co(c[0]));
    cla_4bit cla1(.A(A[7:4]), .B(B[7:4]), .Ci(c[0]), .S(S[7:4]), .G(g[1]), .P(p[1]), .Co(c[1]));
    cla_4bit cla2(.A(A[11:8]), .B(B[11:8]), .Ci(c[1]), .S(S[11:8]), .G(g[2]), .P(p[2]), .Co(c[2]));
    cla_4bit cla3(.A(A[15:12]), .B(B[15:12]), .Ci(c[2]), .S(S[15:12]), .G(g[3]), .P(p[3]), .Co(c[3]));

    // Instantiate the 16-bit lookahead carry unit
    carry_lookahead_unit_16bit clu(
        .G(g), 
        .P(p), 
        .C0(1'b0), 
        .C16(c[3])
    );

    // The upper 16 bits of the adder
    cla_16bit cla_upper(
        .A(A[31:16]), 
        .B(B[31:16]), 
        .C0(c[3]), 
        .S(S[31:16]), 
        .Gx(), 
        .Px(), 
        .C32(C32)
    );

endmodule


module cla_4bit(
    input [3:0] A, B,
    input Ci,
    output [3:0] S,
    output G, P,
    output Co
);
    // Internal wires for generate, propagate, and carry
    wire [3:0] g, p, c;

    // Calculate generate and propagate for each bit
    assign g = A & B;
    assign p = A ^ B;

    // Calculate carries
    assign c[0] = Ci;
    assign c[1] = g[0] | (p[0] & c[0]);
    assign c[2] = g[1] | (p[1] & c[1]);
    assign c[3] = g[2] | (p[2] & c[2]);
    assign Co = g[3] | (p[3] & c[3]);

    // Output generate and propagate for the lookahead carry unit
    assign G = g[3] | (p[3] & g[2]) | (p[3] & p[2] & g[1]) | (p[3] & p[2] & p[1] & g[0]);
    assign P = p[3] & p[2] & p[1] & p[0];

    // Calculate the sum
    assign S = p ^ c;

endmodule


module carry_lookahead_unit_16bit(
    input [3:0] G, // Generate from each 4-bit CLA
    input [3:0] P, // Propagate from each 4-bit CLA
    input C0,      // Input carry
    output [3:0] C // Output carries for each 4-bit CLA block
);
    // Calculate carries based on generate and propagate signals
    assign C[0] = G[0] | (P[0] & C0);
    assign C[1] = G[1] | (P[1] & C[0]);
    assign C[2] = G[2] | (P[2] & C[1]);
    assign C[3] = G[3] | (P[3] & C[2]);

endmodule


module cla_16bit(
    input [15:0] A,
    input [15:0] B,
    input C0,
    output [15:0] S,
    output Gx,
    output Px,
    output C32
);
    wire [3:0] g, p;
    wire [3:0] c; // Carry signals within the 16-bit block

    // Instantiating the lower 8-bit CLA
    cla_4bit lower_cla0(
        .A(A[3:0]),
        .B(B[3:0]),
        .Ci(C0),
        .S(S[3:0]),
        .G(g[0]),
        .P(p[0]),
        .Co(c[0])
    );

    // Instantiating the upper 8-bit CLA
    cla_4bit upper_cla0(
        .A(A[7:4]),
        .B(B[7:4]),
        .Ci(c[0]),
        .S(S[7:4]),
        .G(g[1]),
        .P(p[1]),
        .Co(c[1])
    );

    // Continuing the instantiation for the next two 4-bit blocks
    cla_4bit lower_cla1(
        .A(A[11:8]),
        .B(B[11:8]),
        .Ci(c[1]),
        .S(S[11:8]),
        .G(g[2]),
        .P(p[2]),
        .Co(c[2])
    );

    cla_4bit upper_cla1(
        .A(A[15:12]),
        .B(B[15:12]),
        .Ci(c[2]),
        .S(S[15:12]),
        .G(g[3]),
        .P(p[3]),
        .Co(c[3])
    );

    // Calculate the overall generate and propagate signals for the 16-bit CLA
    assign Gx = g[3] | (p[3] & g[2]) | (p[3] & p[2] & g[1]) | (p[3] & p[2] & p[1] & g[0]);
    assign Px = p[3] & p[2] & p[1] & p[0];

    // The carry-out of the entire 16-bit block is the carry-out of the last 4-bit block
    assign C32 = c[3];

endmodule
