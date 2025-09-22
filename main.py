import emu
processor6502 = emu.SixFiveOTwo(file="mem.b")

if input("do you wanna access the memory debuuger rn>") == "y": processor6502.memoryDisplayer()

processor6502.convert("main.asm") #convert to mem.b
processor6502.start()
