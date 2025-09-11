import string

class ASMToBytesCompilier:
	def __init__(self, file):
		self.file = file
		#my own homemade 6502 optable!
		self.optable = {
		"BRK impl": {"ascii": "BRK", "bytes": 00}, 
		"NOP impl": {"ascii": "NOP", "bytes": 0xEA}, 
		"NOP impl": {"ascii": "NOP", "bytes": 0xEA}, 
		"LDA zpg": {"ascii": "LDA", "bytes": 0xA5},
		"LDA imm": {"ascii": "LDA", "bytes": 0xA9}, 
		
		}
	def convertInto(self, asmString, outputfile="memory"):
		pass
class RAM:
	def __init__(self):
		self.memory = open("mem", "rb")


class Processor:

	def __init__(self):
		self.accumulator = 0x0000 #current memory location, or "A"
		self.registerX = 0x0000
		self.registerY = 0x0000
		self.programCounter = 0x0000
		self.memory = [0x0000] * 1024 #1 KB of (emulated) storage!
		self.zeroFlag = False
		self.negativeFlag = False
		self.debugVerbose = False
		self.isAppleOne = True #emulates the annoying apple 1 architecture
		self.appleArc = Apple1Hardware()
		self.pointerLabels = []
	def displayDebugInfo(self, detailed=False):
		print("A: " + str(self.accumulator))
		### TODO add robust check for every command and memory operation 
	def assignLabelPointers(self, programText):
		"""Assigns the location of pointers based on ASM
		labels and stores them into a self.list"""
		for programstring in programText:
			#goes through the program text and finds
			#the correct text
			if ":" in programstring:
				#if it contains this (label mark)
				programstring.split(":")[0].strip() # split and get the title and rstrip
				print(programstring)
				self.pointerLabels.append({"name": programstring, "pointer": programCounter})

def instructionOperate(self, instructionInBytes):
		"""Executes a 6502 instruction as emulated"""
		try: #comment removal
			trueinstruction, comment = instruction.split(";")
		except ValueError:
			trueinstruction = instruction #no comment
		try:	#split value and instruction
			global instructionNamespace
			global instructionValue
			instructionNamespace, instructionValue = trueinstruction.split()
		except Exception as e:
			print("program terminated")
			print(e)
			return False
		#increment program counter
		self.programCounter += 1

		#define hex namespace if exists
		global hexValue
		try:
			if instructionValue[0] == "#": #this is a real value
				hexValue = int(instructionValue[1:].replace("$", "").replace(",", " + "), 16)
			else:
				#this is a pointer, difference is the [1:] is not needed
				hexValue = int(instructionValue.replace("$", "").replace(",", " + "), 16)
		except Exception as e:
			print("eeeee")
			print(e)
			#fail silently
			if self.debugVerbose == True:
					print("No hexvalue")

		if instructionNamespace == "NOP":
			#NOP - does nothing
			pass #hard to understand, but nothing happens
		if instructionNamespace == "LDA":
			#LDA - stores a byte or a value at a register
			#first we have to determine based on the ruleset
			#whether the LDA is accessing and storing the value
			#located at the point to the accumulator
			#which is determined by whether the InstructionValue's
			#pointer == #$01 (this means ADD the value to the acc)
			#or i
			if instructionValue[0] == "#": # immediate (load the value given instead 
			#of the memory pointer.
				self.accumulator = int(instructionValue.replace("#", "").replace("$", "").replace(",", " + "), 16)
				
				#ZEROFLAG
				if int(instructionValue.replace("#", "").replace("$", "").replace(",", " + "), 16) == 0:
					self.zeroFlag = True
				else:
					self.zeroFlag = False
			#otherwise we need to load the pointer where the memory is located
			if instructionValue[0] == "$":
				baseTenValue = self.memory[int(instructionValue.replace("$", "0x"), 0)]
				#convert pointer to integer to memory value, the return memory's value (in hex!!!)
				self.accumulator = baseTenValue	
				
				#ZEROFLAG
				if baseTenValue == 0:
					self.zeroFlag = True
				else:
					self.zeroFlag = False
		if instructionNamespace == "STA":
			#STA - stores value in register at the accumulator
			#i was confused when i read this ^ so
			# accumulator >>>>> register specified in hex
			if self.isAppleOne and hexValue > 53248: #oh boy
				self.appleArc.handleDAddress(self, instructionNamespace, instructionValue) #pass it to the dbus and handle it there
				return True
			if self.debugVerbose:
				print("OLD VALUE AT MEMORY ADDR" + instructionValue)
				print(instructionValue + " | " + str(self.memory[int(instructionValue.replace("$", ""), 16)]))
			#store accumulator, or a function which takes the value
			#in the accumulator and stores it into memory at a location
			#i don't fully understand but python can take any base value and access it's according
			#index in a list so let's just go with it
			self.memory[int(instructionValue.replace("$", ""), 16)] = self.accumulator
			#more debug stuff
			if self.debugVerbose:
				print("NEW VALUE AT MEMORY ADDR ")
				print(self.memory[int(instructionValue.replace("$", ""), 16)])
			#ZEROFLAG
			if self.memory[int(instructionValue.replace("$", ""), 16)] == 0:
				self.zeroFlag = True
			else:
				self.zeroFlag = False
		if instructionNamespace == "ADC":
			## ADC -- adds value (either memory location or hex value)
			## to the accumulator
			if self.instructionValue[0] == "$": #this should be a pointer and not a value
				self.instructionValue = int(instructionValue[1:].replace("$", ""), 16)
		if instructionNamespace == "TAX":
			## TAX- sets the value in the A register to X
			self.registerX = self.accumulator

			##ZEROFLAG
			if self.accumulator == 0:
				self.zeroFlag = True#set zeroflag because 6502
			else:
				self.zeroFlag = False
		if instructionNamespace == "INX":
			##INX -- increments the value in the X by one
			if self.registerX == 255:
				self.registerX = 0
				self.zeroFlag = True
			else:
				self.registerX += 1
				self.zeroFlag = False
		if instructionNamespace == "DEX":
			##DEX -- deincrements the value in the X by one
			self.registerX -= 1
			if self.registerX == 0:
				self.zeroFlag = True
			elif self.registerX == -1:
				self.zeroFlag = False
				self.registerX = 255
			else:	
				self.zeroFlag = False
		if instructionNamespace == "TAY":
			## TAX- sets the value in the A register to Y
			self.registerY = self.accumulator

			##ZEROFLAG
			if self.accumulator == 0:
				self.zeroFlag = True#set zeroflag because 6502
			else:
				self.zeroFlag = False
		if instructionNamespace == "INY":
			##INY -- increments the value in the Y by one
			if self.registerY == 255:
				self.registerY = 0
				self.zeroFlag = True
			else:
				self.registerY += 1
				self.zeroFlag = False
		if instructionNamespace == "DEX":
			##DEY -- deincrements the value in the Y by one
			self.registerY -= 1
			if self.registerY == 0:
				self.zeroFlag = True
			elif self.registerY == -1:
				self.zeroFlag = False
				self.registerY = 255
			else:	
				self.zeroFlag = False
		if instructionNamespace == "BRK":
			## BRK, return out of computer, terminate
			return "BREAK"




	def instructionOperateLegacyString(self, instruction):
		"""Executes a 6502 instruction as emulated"""
		try: #comment removal
			trueinstruction, comment = instruction.split(";")
		except ValueError:
			trueinstruction = instruction #no comment
		try:	#split value and instruction
			global instructionNamespace
			global instructionValue
			instructionNamespace, instructionValue = trueinstruction.split()
		except Exception as e:
			print("program terminated")
			print(e)
			return False
		#increment program counter
		self.programCounter += 1

		#define hex namespace if exists
		global hexValue
		try:
			if instructionValue[0] == "#": #this is a real value
				hexValue = int(instructionValue[1:].replace("$", "").replace(",", " + "), 16)
			else:
				#this is a pointer, difference is the [1:] is not needed
				hexValue = int(instructionValue.replace("$", "").replace(",", " + "), 16)
		except Exception as e:
			print("eeeee")
			print(e)
			#fail silently
			if self.debugVerbose == True:
					print("No hexvalue")

		if instructionNamespace == "NOP":
			#NOP - does nothing
			pass #hard to understand, but nothing happens
		if instructionNamespace == "LDA":
			#LDA - stores a byte or a value at a register
			#first we have to determine based on the ruleset
			#whether the LDA is accessing and storing the value
			#located at the point to the accumulator
			#which is determined by whether the InstructionValue's
			#pointer == #$01 (this means ADD the value to the acc)
			#or i
			if instructionValue[0] == "#": # immediate (load the value given instead 
			#of the memory pointer.
				self.accumulator = int(instructionValue.replace("#", "").replace("$", "").replace(",", " + "), 16)
				
				#ZEROFLAG
				if int(instructionValue.replace("#", "").replace("$", "").replace(",", " + "), 16) == 0:
					self.zeroFlag = True
				else:
					self.zeroFlag = False
			#otherwise we need to load the pointer where the memory is located
			if instructionValue[0] == "$":
				baseTenValue = self.memory[int(instructionValue.replace("$", "0x"), 0)]
				#convert pointer to integer to memory value, the return memory's value (in hex!!!)
				self.accumulator = baseTenValue	
				
				#ZEROFLAG
				if baseTenValue == 0:
					self.zeroFlag = True
				else:
					self.zeroFlag = False
		if instructionNamespace == "STA":
			#STA - stores value in register at the accumulator
			#i was confused when i read this ^ so
			# accumulator >>>>> register specified in hex
			if self.isAppleOne and hexValue > 53248: #oh boy
				self.appleArc.handleDAddress(self, instructionNamespace, instructionValue) #pass it to the dbus and handle it there
				return True
			if self.debugVerbose:
				print("OLD VALUE AT MEMORY ADDR" + instructionValue)
				print(instructionValue + " | " + str(self.memory[int(instructionValue.replace("$", ""), 16)]))
			#store accumulator, or a function which takes the value
			#in the accumulator and stores it into memory at a location
			#i don't fully understand but python can take any base value and access it's according
			#index in a list so let's just go with it
			self.memory[int(instructionValue.replace("$", ""), 16)] = self.accumulator
			#more debug stuff
			if self.debugVerbose:
				print("NEW VALUE AT MEMORY ADDR ")
				print(self.memory[int(instructionValue.replace("$", ""), 16)])
			#ZEROFLAG
			if self.memory[int(instructionValue.replace("$", ""), 16)] == 0:
				self.zeroFlag = True
			else:
				self.zeroFlag = False
		if instructionNamespace == "ADC":
			## ADC -- adds value (either memory location or hex value)
			## to the accumulator
			if self.instructionValue[0] == "$": #this should be a pointer and not a value
				self.instructionValue = int(instructionValue[1:].replace("$", ""), 16)
		if instructionNamespace == "TAX":
			## TAX- sets the value in the A register to X
			self.registerX = self.accumulator

			##ZEROFLAG
			if self.accumulator == 0:
				self.zeroFlag = True#set zeroflag because 6502
			else:
				self.zeroFlag = False
		if instructionNamespace == "INX":
			##INX -- increments the value in the X by one
			if self.registerX == 255:
				self.registerX = 0
				self.zeroFlag = True
			else:
				self.registerX += 1
				self.zeroFlag = False
		if instructionNamespace == "DEX":
			##DEX -- deincrements the value in the X by one
			self.registerX -= 1
			if self.registerX == 0:
				self.zeroFlag = True
			elif self.registerX == -1:
				self.zeroFlag = False
				self.registerX = 255
			else:	
				self.zeroFlag = False
		if instructionNamespace == "TAY":
			## TAX- sets the value in the A register to Y
			self.registerY = self.accumulator

			##ZEROFLAG
			if self.accumulator == 0:
				self.zeroFlag = True#set zeroflag because 6502
			else:
				self.zeroFlag = False
		if instructionNamespace == "INY":
			##INY -- increments the value in the Y by one
			if self.registerY == 255:
				self.registerY = 0
				self.zeroFlag = True
			else:
				self.registerY += 1
				self.zeroFlag = False
		if instructionNamespace == "DEX":
			##DEY -- deincrements the value in the Y by one
			self.registerY -= 1
			if self.registerY == 0:
				self.zeroFlag = True
			elif self.registerY == -1:
				self.zeroFlag = False
				self.registerY = 255
			else:	
				self.zeroFlag = False
		if instructionNamespace == "BRK":
			## BRK, return out of computer, terminate
			return "BREAK"


	#schoonover	
class Apple1Hardware:
	def __init__(self):
		self.memoryD = [0] * 255
		# Generate a full 7-bit ASCII table (0-127) for Apple-1
		self.characters = [chr(i) for i in range(128)]
	def handleDAddress(self, instance6502, instructionNamespace, instructionValue):
		if instructionNamespace == "STA":
			if instructionValue == "$D012":
				#This is the character char
				self.memoryD[12] = instance6502.accumulator
				#since STA was accessed, display a char 
				print(self.characters[self.memoryD[12]])
			if instructionValue == "$D013":
				#This is the video control
				self.memoryD[12] = 1 #python will always be ready to write

				



