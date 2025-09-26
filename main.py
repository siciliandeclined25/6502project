import emu
import os
debugme = True if input("do you want to enable debug mode? (y/n): ").lower() == "y" else False
#print(debugme)
#if debugme:
    #if input("do you wanna access the memory debuuger rn>") == "y": processor6502.memoryDisplayer()
os.system('ls')
processor6502 = emu.SixFiveOTwo(file="mem.b")
processor6502.convert(input('choose a file to convert> '), debug=debugme) #convert to mem.b
processor6502.start(debug=debugme)
