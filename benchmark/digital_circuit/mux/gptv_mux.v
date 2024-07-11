module mux (
    input              clk_a,
    input              clk_b,
    input              arstn,
    input              brstn,
    input      [3:0]   data_in,
    input              data_en,
    output reg [3:0]   dataout
);

    // Synchronization registers for data and enable signals
    reg [3:0] datareg_a;
    reg       data_en_a;

    reg [3:0] datareg_b1, datareg_b2;
    reg       data_en_b1, data_en_b2, data_en_b3;

    // Asynchronous reset for domain A
    always @(posedge clk_a or negedge arstn) begin
        if (!arstn) begin
            datareg_a <= 4'b0;
            data_en_a <= 1'b0;
        end else begin
            datareg_a <= data_in;
            data_en_a <= data_en;
        end
    end

    // Synchronize the data_en signal to domain B
    always @(posedge clk_b or negedge brstn) begin
        if (!brstn) begin
            data_en_b1 <= 1'b0;
            data_en_b2 <= 1'b0;
            data_en_b3 <= 1'b0;
        end else begin
            data_en_b1 <= data_en_a;
            data_en_b2 <= data_en_b1;
            data_en_b3 <= data_en_b2;
        end
    end

    // Synchronize the data signal to domain B
    always @(posedge clk_b) begin
        if (!data_en_b3) begin
            datareg_b1 <= 4'b0;
            datareg_b2 <= 4'b0;
        end else begin
            datareg_b1 <= datareg_a;
            datareg_b2 <= datareg_b1;
        end
    end

    // Output assignment with registered data from domain B
    always @(posedge clk_b or negedge brstn) begin
        if (!brstn) begin
            dataout <= 4'b0;
        end else begin
            // Check if the enable signal has been stable for 3 clock cycles
            if (data_en_b1 && data_en_b2 && data_en_b3) begin
                dataout <= datareg_b2; // Synchronized data
            end
        end
    end

endmodule
