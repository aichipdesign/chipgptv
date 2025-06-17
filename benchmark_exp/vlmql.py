from typing import Any


class vlmql:
    def __init__(self,func) -> None:
        self.func=func
    def set_mode(prompt):
        vlmql.mode = f"The output block of the hardware should have {prompt}."
    def run():
        if vlmql.lvm==None and not vlmql.img_path==None:
            raise Exception("Type error")
        print(f"Please act as a Verilog programmer. {vlmql.mode} ")
        print("Generate the following hardware according to the prompt respectively.")
        print(f"The code should only consider {vlmql.constrain}.")
        for item in vlmql.func:
            print(f"{item}")
        print(f"Please provides the eda script using EDA tool: {vlmql.tooltype}.")
        print(f"The EDA script should be {vlmql.edaarg}.")
        print(f"<img>{vlmql.img_path}</img>")
    def lvm(lmtype):
        vlmql.lvm=lmtype
    def llm(lmtype):
        vlmql.llm=lmtype
    def image_path(image):
        vlmql.img_path=image
    def function(*args):
        vlmql.func = []
        for item in args:
            vlmql.func.append(item)
    def eda_flow(edaarg):
        vlmql.edaarg=edaarg
    def eda_tool(tooltype):
        vlmql.tooltype=tooltype
    def module_constrain(cons):
        vlmql.constrain=cons
    def __call__(self, *args: Any, **kwds: Any) -> Any:
       print("----The generating prompt----")
       res = self.func(*args,**kwds)
       return res

@vlmql
def pipeline_5stage():
    # mode declaration
    vlmql.set_mode("func_block")
    # large model declaration
    vlmql.lvm("gpt4v")
    vlmql.llm("gpt4v")
    vlmql.image_path("5stage.png")
    # function declaration
    vlmql.function(
    "The image show a 5 stage pipeline to add two number",
    "the execution stage add two number from register r1 and register r0",
    "the write back stage write the result to register r2",
    )
    # EDA agent flow description
    vlmql.eda_flow("the area should large than (1000,1000)") # choose 
    vlmql.eda_tool("siliconcompiler")
    # constraint statement
    vlmql.module_constrain("execute stage")
    return vlmql.run()


pipeline_5stage()