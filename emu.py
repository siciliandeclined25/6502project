







class Processor:

	def __init__(self):
		self.accumulator = 0x0000 #current memory location, or "A"
		self.registerX = 0
		self.registerY = 0
		self.programCounter = 0
		self.memory = [0x0000] * 1024 #1 KB of (emulated) storage!
		self.zeroFlag = 0
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
		if instructionNamespace == "NOP":
			pass
		if instructionNamespace == "LDA":
			#first we have to determine based on the ruleset
			#whether the LDA is accessing and storing the value
			#located at the point to the accumulator
			#which is determined by whether the InstructionValue's
			#pointer == #$01 (this means ADD the value to the acc)
			#or i
			if instructionValue[0] == "#": # immediate (load the value given instead 
			#of the memory pointer.
				self.accumulator = int(instructionValue.replace("#", "").replace("$", ""), 16)
			#otherwise we need to load the pointer where the memory is located
			if instructionValue[0] == "$":
				baseTenValue = self.memory[int(instructionValue.replace("$", "0x"), 0)]
				#convert pointer to integer to memory value, the return memory's value (in hex!!!)
				self.accumulator = baseTenValue	
		if instructionNamespace == "STA":
			if self.debugVerbose:
				print("OLD VALUE AT MEMORY ADDR" + instructionValue)
				print(instructionValue + " | " + str(self.memory[int(instructionValue.replace("$", ""), 16)]))
			#store accumulator, or a function which takes the value
			#in the accumulator and stores it into memory at a location
			#i don't fully understand but python can take any base value and access it's according
			#index in a list so let's just go with it
			self.memory[int(instructionValue.replace("$", ""), 16)] = self.accumulator
			if self.debugVerbose:
				print("NEW VALUE AT MEMORY ADDR ")
				print(self.memory[int(instructionValue.replace("$", ""), 16)])
					
	#schoonover	
