module fsm(
    input wire CLK,    // Clock input
    input wire RST,    // Reset input
    input wire IN,     // Serial bit input
    output reg MATCH   // MATCH output
);

    // State declaration using parameters for better readability
    parameter S0 = 3'b000,
              S1 = 3'b001,
              S2 = 3'b010,
              S3 = 3'b011,
              S4 = 3'b100,
              S5 = 3'b101;

    // Current state and next state variables
    reg [2:0] current_state, next_state;

    // State transition logic (sequential block)
    always @(posedge CLK or posedge RST) begin
        if (RST) begin
            current_state <= S0; // Reset to initial state S0
        end else begin
            current_state <= next_state;
        end
    end

    // Next state logic (combinational block)
    always @(*) begin
        // Default next state is the same as the current state
        next_state = current_state;

        case(current_state)
            S0: begin
                if (IN == 1'b1) begin
                    next_state = S1;
                end
            end
            S1: begin
                if (IN == 1'b0) begin
                    next_state = S2;
                end else begin
                    next_state = S1; // Loop in state S1 if IN is not 0
                end
            end
            S2: begin
                if (IN == 1'b0) begin
                    next_state = S3;
                end else begin
                    next_state = S1; // Go back to state S1 if IN is not 0
                end
            end
            S3: begin
                if (IN == 1'b1) begin
                    next_state = S4;
                end else begin
                    next_state = S0; // Reset to S0 if IN is not 1
                end
            end
            S4: begin
                if (IN == 1'b1) begin
                    next_state = S5;
                end else begin
                    next_state = S0; // Reset to S0 if IN is not 1
                end
            end
            S5: begin
                // Stay in S5 if the last input was 1, otherwise reset to S0
                next_state = (IN == 1'b1) ? S5 : S0;
            end
            default: begin
                next_state = S0; // Handle any undefined states
            end
        endcase
    end

    // Output logic (combinational block)
    always @(*) begin
        // MATCH is high only in state S5
        MATCH = (current_state == S5) ? 1'b1 : 1'b0;
    end

endmodule
