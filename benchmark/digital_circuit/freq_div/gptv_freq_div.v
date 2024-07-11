module freq_div(
    input CLK_in,
    input RST,
    output reg CLK_50,
    output reg CLK_10,
    output reg CLK_1
);

// Define counters
reg [5:0] counter_2; // This will count up to 2 for 50MHz output
reg [3:0] counter_5; // This will count up to 5 for 10MHz output
reg [6:0] counter_50; // This will count up to 50 for 1MHz output

// Initialize all counters and outputs
initial begin
    counter_2 = 0;
    counter_5 = 0;
    counter_50 = 0;
    CLK_50 = 0;
    CLK_10 = 0;
    CLK_1 = 0;
end

// Counter for CLK_50 (Toggle every 1 clock cycle to divide by 2)
always @(posedge CLK_in or posedge RST) begin
    if (RST) begin
        counter_2 <= 0;
        CLK_50 <= 0;
    end else if (counter_2 == 1) begin
        counter_2 <= 0;
        CLK_50 <= ~CLK_50;
    end else begin
        counter_2 <= counter_2 + 1;
    end
end

// Counter for CLK_10 (Toggle every 5 clock cycles to divide by 10)
always @(posedge CLK_in or posedge RST) begin
    if (RST) begin
        counter_5 <= 0;
        CLK_10 <= 0;
    end else if (counter_5 == 4) begin
        counter_5 <= 0;
        CLK_10 <= ~CLK_10;
    end else begin
        counter_5 <= counter_5 + 1;
    end
end

// Counter for CLK_1 (Toggle every 50 clock cycles to divide by 100)
always @(posedge CLK_in or posedge RST) begin
    if (RST) begin
        counter_50 <= 0;
        CLK_1 <= 0;
    end else if (counter_50 == 49) begin
        counter_50 <= 0;
        CLK_1 <= ~CLK_1;
    end else begin
        counter_50 <= counter_50 + 1;
    end
end

endmodule
