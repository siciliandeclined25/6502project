







class Processor:

	def __init__(self):
		self.accumulator = 0x0000 #current memory location, or "A"
		self.registerX = 0
		self.registerY = 0
		self.programCounter = 0
		self.memory = [0x0000] * 1024 #1 KB of (emulated) storage!
		self.zeroFlag = False
		self.negativeFlag = False
		self.debugVerbose = False
	def displayDebugInfo(self, detailed=False):
		print("A: " + str(self.accumulator))
		### TODO add robust check for every command and memory operation 
	def instructionOperate(self, instruction):
		try: #comment removal
			trueinstruction, comment = instruction.split(";")
		except ValueError:
			trueinstruction = instruction #no comment
		try:	#split value and instruction
			instructionNamespace, instructionValue = trueinstruction.split()
		except ValueError as e:
			print("program terminated")
			print(e)
			return False
		#increment program counter
		self.programCounter += 1
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


	#schoonover	
