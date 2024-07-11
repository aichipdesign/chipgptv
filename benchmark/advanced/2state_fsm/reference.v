// State machine design
module state_machine(
  input a,
  input b,
  input clk,
  input rst,
  output reg [3:0] state
);
parameter S0 = 4'b1001;
parameter S1 = 4'b1000;
always @(posedge clk) begin
  if (rst) begin
    state <= S0;
  end
  else begin
    case (state)
    S0: if (a & ~b) state <= S1;
    S1: if (a & ~b) state <= S0;
    default: state <= S1;
    endcase
  end
end
endmodule