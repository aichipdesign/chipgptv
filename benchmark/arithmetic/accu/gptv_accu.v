module accu (
    input               clk,
    input               rst_n,
    input       [7:0]   data_in,
    input               valid_a,
    output reg          ready_a,
    input               ready_b,
    output reg          valid_b,
    output reg  [9:0]   data_out
);

    // Internal signal to hold the accumulated value
    reg [9:0] sum;
    // Counter to track the number of received data items
    reg [1:0] data_count;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            // Reset the internal state
            sum <= 0;
            data_count <= 0;
            data_out <= 0;
            valid_b <= 0;
            ready_a <= 0;
        end else begin
            // Manage ready/valid signals
            ready_a <= !valid_b || ready_b; // Ready if not valid or downstream is ready
            valid_b <= (data_count == 2'b11) && valid_a; // Valid if 4th data and valid input

            if (ready_a && valid_a) begin
                // Accept new data and accumulate
                sum <= sum + data_in;
                data_count <= data_count + 1;

                // Check if this is the 4th data item
                if (data_count == 2'b11) begin
                    // Output the sum
                    data_out <= sum + data_in; // Include the current data_in in the sum
                    sum <= 0; // Reset sum for next cycle
                    data_count <= 0; // Reset count for next cycle
                end
            end

            // If valid data is not taken by downstream, keep valid high
            if (valid_b && !ready_b) begin
                valid_b <= 1;
            end
        end
    end

endmodule
