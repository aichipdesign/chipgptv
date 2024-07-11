module verified_fsm5 (
    input IN, CLK, RST,
    output reg MATCH
);

    reg [2:0] ST_cr, ST_nt;

    parameter s0 = 3'b000, s1 = 3'b001, s2 = 3'b010, s3 = 3'b011, s4 = 3'b100;

    always @(posedge CLK or posedge RST) begin
        if (RST)
            ST_cr = s0;
        else
            ST_cr = ST_nt;
    end

    always @* begin
        case (ST_cr)
            s0: ST_nt = (IN == 0) ? s0 : s1;
            s1: ST_nt = (IN == 0) ? s1 : s2;
            s2: ST_nt = (IN == 0) ? s2 : s3;
            s3: ST_nt = (IN == 0) ? s3 : s4;
            s4: ST_nt = (IN == 0) ? s4 : s0;
            //s5: ST_nt = (IN == 0) ? s5 : s0;
            default: ST_nt = s0; // Add a default assignment
        endcase
    end

    always @(posedge CLK or posedge RST) begin
        if (RST)
            MATCH = 0;
        else if (ST_cr == s4)
            MATCH = 1;
        else
            MATCH = 0;
    end

endmodule
