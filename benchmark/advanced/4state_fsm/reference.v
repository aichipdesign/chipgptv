module verified_fsm4 (
    input IN, CLK, RST,
    output reg MATCH
);

    reg [1:0] ST_cr, ST_nt;

    parameter s0 = 2'b00, s1 = 2'b01, s2 = 2'b10, s3 = 2'b11;

    always @(posedge CLK or posedge RST) begin
        if (RST)
            ST_cr = s0;
        else
            ST_cr = ST_nt;
    end

    always @* begin
        case (ST_cr)
            s0: ST_nt = (IN == 0) ? s3 : s1;
            s1: ST_nt = (IN == 0) ? s0 : s2;
            s2: ST_nt = (IN == 0) ? s1 : s3;
            s3: ST_nt = (IN == 0) ? s2 : s0;
            //s4: ST_nt = (IN == 0) ? s4 : s0;
            //s5: ST_nt = (IN == 0) ? s5 : s0;
            default: ST_nt = s0; // Add a default assignment
        endcase
    end

    always @(posedge CLK or posedge RST) begin
        if (RST)
            MATCH = 0;
        else if (ST_cr == s3)
            MATCH = 1;
        else
            MATCH = 0;
    end

endmodule
