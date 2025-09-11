import emu

processor6502 = emu.SixFiveOTwo(file="mem.b")
processor6502.convert("main.asm") #convert to mem.b
processor6502.start()
