DESIGN = reference
TESTBENCH = testbed


VERILATOR = verilator


EXEC = simulate

VERILATOR_FLAGS = --cc --exe --trace -Wall


COMPILE_FLAGS = -O2

all: $(EXEC)

$(EXEC): $(DESIGN).v $(TESTBENCH).v
	$(VERILATOR) $(VERILATOR_FLAGS) $(DESIGN).v $(TESTBENCH).v 


%.cpp: %.v
	$(VERILATOR) $(VERILATOR_FLAGS) $^
	$(CC) $(COMPILE_FLAGS) -o $@ V$(notdir $(DESIGN)).cpp

run: $(EXEC) 
	./$(EXEC)

clean:
	rm -f $(EXEC) V$(DESIGN).*
	rm -f -r obj_dir

.PHONY: clean