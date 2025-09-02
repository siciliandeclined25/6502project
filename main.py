import emu
processor6502 = emu.Processor()
mainasm = open('main.asm', 'r').read().split("\n")
i = 0
debug = False
while True:
	if i == len(mainasm)-1:
		print("eof")
		break
	processor6502.instructionOperate(mainasm[i])
	i += 1
	if debug:
		print("OPERATION: " + str(mainasm[i]))
		processor6502.displayDebugInfo()
