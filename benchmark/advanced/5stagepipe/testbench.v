module tb_pipeline();
// Inputs
reg clk; 
reg [31:0] reg_file[0:31];
// Pipeline signals
wire [31:0] inst, pc, op1, op2, result, mem_data;
wire [4:0] rs1, rs2, rd, rd1, rd2;
wire [1:0] op;
reg [31:0] instr_mem[0:31];
reg rst;
wire [31:0] res_reg_file[0:31];
// Pipeline stages
fetch_stage fetch (.clk(clk), .inst(inst), .rst(rst), .instr_mem_in(instr_mem));
decode_stage decode (
  .clk(clk),
  .inst(inst),
  .rs1(rs1),
  .rs2(rs2),
  .op(op),
  .rd(rd)
);
execute_stage execute (
  .clk(clk),
  .rs1(rs1),
  .rs2(rs2),
  .reg_file(reg_file),
  .op(op),
  .result(result),
  .rdin1(rd),
  .rdout1(rd1)
);
memory_stage memory(.clk(clk), .alu_result(result), .mem_data(mem_data), .rdin2(rd1), .rdout2(rd2));
writeback_stage writeback (
  .clk(clk),
  .mem_data(mem_data),
  .rd(rd2),
  .reg_file(res_reg_file)
);
initial begin
	rst = 1;
	#5 rst = 0;
end
// Clock 
initial begin
	clk=0;
	forever #5 clk=~clk;
end
// Instruction memory 

initial begin
  // Test program
  instr_mem[0] = {`ADD_INST, 5'd1, 5'd2, 5'd3, 15'd3};
  instr_mem[1] = {`SUB_INST, 5'd1, 5'd2, 5'd2, 15'd3};
  instr_mem[2] = {2'b11, 5'd3, 5'd1, 5'd2, 15'd3};
  // Initialize
  reg_file[1] = 20;
  reg_file[2] = 10;
  // Run 2 cycles
  #60;
  // Verify result
  if(res_reg_file[3] !== 10) 
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
