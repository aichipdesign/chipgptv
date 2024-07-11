module alu (
    input [31:0] a, b,
    input [5:0] aluc,
    output reg [31:0] r,
    output zero,
    output carry,
    output negative,
    output overflow,
    output flag
);

// Define parameters for operations
parameter ADD  = 6'b100000;
parameter ADDU = 6'b100001;
parameter SUB  = 6'b100010;
parameter SUBU = 6'b100011;
parameter AND  = 6'b100100;
parameter OR   = 6'b100101;
parameter XOR  = 6'b100110;
parameter NOR  = 6'b100111;
parameter SLT  = 6'b101010;
parameter SLTU = 6'b101011;
parameter SLL  = 6'b000000;
parameter SRL  = 6'b000010;
parameter SRA  = 6'b000011;
parameter SLLV = 6'b000100;
parameter SRLV = 6'b000110;
parameter SRAV = 6'b000111;
parameter LUI  = 6'b001111;

// Internal signal declaration
reg [31:0] result;
reg carry_out;
reg overflow_flag;
reg negative_flag;
reg zero_flag;
reg slt_flag;

assign zero = (result == 32'b0);
assign carry = carry_out;
assign negative = negative_flag;
assign overflow = overflow_flag;
assign flag = slt_flag;

always @(*) begin
    carry_out = 0;
    overflow_flag = 0;
    negative_flag = 0;
    slt_flag = 0;
    case (aluc)
        ADD: {carry_out, result} = a + b;
        ADDU: result = a + b;
        SUB: {carry_out, result} = a - b;
        SUBU: result = a - b;
        AND: result = a & b;
        OR: result = a | b;
        XOR: result = a ^ b;
        NOR: result = ~(a | b);
        SLT: {slt_flag, result} = $signed(a) < $signed(b) ? 32'b1 : 32'b0;
        SLTU: {slt_flag, result} = a < b ? 32'b1 : 32'b0;
        SLL: result = b << a;
        SRL: result = b >> a;
        SRA: result = $signed(b) >>> a;
        SLLV: result = b << (a & 32'h1F);
        SRLV: result = b >> (a & 32'h1F);
        SRAV: result = $signed(b) >>> (a & 32'h1F);
        LUI: result = b << 16;
        default: result = 32'hXXXX_XXXX; // Indeterminate result for undefined opcodes
    endcase

    // Set flags
    negative_flag = result[31];
    overflow_flag = (aluc == ADD || aluc == SUB) && 
                    ((a[31] == b[31]) && (result[31] != a[31]));

    // 'slt' and 'sltu' flags are set during their case
    r = result; // Assign result to output
end

endmodule
