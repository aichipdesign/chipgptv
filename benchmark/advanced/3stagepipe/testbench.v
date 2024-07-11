module tb_pipeline();
// Inputs
reg clk;
reg [31:0] reg_file[0:31];
reg [31:0] RAM[0:31];
// Pipeline signals 
wire [31:0] inst, result;
reg [31:0] instr_mem[0:31];
reg rst;
// Pipeline stages
fetch_stage fetch (.clk(clk), .inst(inst), .rst(rst), .instr_mem_in(instr_mem));
execute_stage execute (
  .clk(clk),
  .inst(inst),
  .reg_file(reg_file),
  .result(result)
);
writeback_stage writeback (
  .clk(clk),
  .result(result),
  .reg_file(RAM[3])
);
// Cloc3
initial begin
	rst = 1;
	#5 rst = 0;
end
initial begin
	clk=0;
	forever #5 clk=~clk;
end
// Instruction memory

initial begin
  // Instructions
  instr_mem[0] = {`ADD_INST, 5'd1, 5'd2, 5'd3, 15'd0};
  instr_mem[1] = {`SUB_INST, 5'd1, 5'd2, 5'd2, 15'd0};
  instr_mem[2] = {2'b11, 5'd3, 5'd1, 5'd2, 15'd0};
  // Initialize reg file
  reg_file[1] = 10;
  reg_file[2] = 20;

  // Run 2 cycles
  #30;
  // Verify result
  if(RAM[3] !== 30) 
    $display("ERROR: Result mismatch");
  else
    $display("design passed");
  
  $finish;
end

initial begin
	$dumpfile("pipeline_3stages.vcd");
	$dumpvars;
end

endmodule
