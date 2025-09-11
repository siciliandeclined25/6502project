import emu
processor6502 = emu.Processor()
mainasm = open('program.asm', 'r').read().split("\n")
debug = False
while True:
	if processor6502.programCounter == len(mainasm):
		print("eof")
		break
	processor6502.instructionOperate(mainasm[processor6502.programCounter])
	if debug:
		print("OPERATION: " + str(mainasm[processor6502.programCounter]))
		processor6502.displayDebugInfo()
