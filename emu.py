import subprocess

class SixFiveOTwo:
  def __init__(self, file="mem.b", size=0x1000):
    self.memoryFile = file
    data = bytes(size) #fill full of empty 0s
    with open(self.memoryFile, "wb") as f:
         f.write(data)
    #my own homemade 6502 optable!
    self.optable = {
    "BRK impl": {"ascii": "BRK", "bytes": 00, "space": 1},
    "NOP impl": {"ascii": "NOP", "bytes": 0xEA,  "space": 1},
    "LDA zpg": {"ascii": "LDA", "bytes": 0xA5,  "space": 2}, #zeropage (0-256)
    "LDA imm": {"ascii": "LDA", "bytes": 0xA9,  "space": 2}, #LDA immediate (just load hex value into accumulator
    "LDA zpg x": {"ascii": "LDA", "bytes": 0xB5,  "space": 2},#zeropage x adds the values in the zeropage address and x and stores them into the accumulator
    "LDA abs": {"ascii": "LDA", "bytes": 0x01}

    }
    #6502 memory variables!!!
    self.a = 0
    self.x = 0
    self.y = 0
    self.pc = 0 #program counter
    self.sp = 0x0100 #stack pointer
    self.nextPCIncrement = 0
  class Memory:
    def getB(self, byteLocation):
      print("bytelocation" + str(byteLocation))
      print(list(open(self.memoryFile, "rb").read()))
      memoryInt = list(open(self.memoryFile, "rb").read())
      return memoryInt[byteLocation]
    def setB(self, byteLocation, byteValue):
      memoryInt = list(open(self.memoryFile, "rb").read())
      memoryInt[byteLocation] = byteValue
      open(self.memoryFile, "wb").write(bytes(memoryInt))
    def memoryDisplayer(self):
      print("MEMORY")
      memoryInt = list(open(self.memoryFile, "rb").read())
      i = 0
      while True:
        print(str(hex(i)) + " > " + str(hex(memoryInt[i])))
        userPrompt = input("(G)oto addr (S)pecial values (C)hange value (Q)uit").lower()
        if userPrompt == "q":
          break
        if userPrompt == "s":
          print("A: " + str(self.a))
          print("X: " + str(self.x))
          print("Y: " + str(self.y))
          print("PC: " + str(self.pc))

        if userPrompt == "g":
          i = int(input("Type in a hex memory address>"), 10)
  def convert(self, fileIn):
    fileToConvert = list(open(fileIn, "r"))
    bytesGiven = []
    byteLocation = 0
    print("CONVERTING....")
    while True:
      print(byteLocation)
      print(fileToConvert)
      if len(fileToConvert) == byteLocation:
          break
      currentByte = fileToConvert[byteLocation]
      print(".", end="")
      trueKeyword = currentByte.split(";")[0].split()[0]
      try:
        trueByteValue = currentByte.split()[1]

      except IndexError:
        print("firstbytenoexist")
        trueByteValue = ""
      #BRK convert
      if trueKeyword == "BRK":
        bytesGiven.append(self.optable["BRK impl"]["bytes"])
        byteLocation += 1
      elif trueKeyword == "NOP":
        bytesGiven.append(self.optable["NOP impl"]["bytes"])
        byteLocation += 1
      elif trueKeyword == "LDA":
        print("LDA reached")
        print(trueByteValue[0])
        if trueByteValue[0] == "#":
          #this is immediate addressing
          #which means the value is
          #being loaded itself into the hex
          bytesGiven.append(self.optable["LDA imm"]["bytes"])
          #adds the current byte value
          bytesGiven.append(int(trueByteValue[2:]))
          #increment by two
          byteLocation += 1
    #this is to add the remaining memory addresses
    bytesGiven += [0] * (4096 - len(bytesGiven))
    open(self.memoryFile, "wb").write(bytes(bytesGiven))
    memoryInt = list(open(self.memoryFile, "rb").read())
    print("MEMORY WRITTEN")
    print(memoryInt)
    input("ready>")
  def executeInstruction(self, opCodeToexecute):
    opInt = int(opCodeToexecute, 16)
    firstValueByte = self.Memory.getB(self, self.pc+1)
    secondValueByte = self.Memory.getB(self, self.pc+2)
    #this is to get the next byte incase the 6502
    #uses it in its operation, and the next after
    if opInt == 0: #BRK impl
      #increment program counter
      self.pc += 1
      return "brk"
    if opInt == 164: #LDA zpg
      self.pc += 2 #two offset for value
      self.a = self.Memory.getB(self.pc+1)
    if opInt == 164: #LDA zpg
      #loads the zeropage value from 0-256
      #into the accumulator
      self.pc += 2 #two offset for value
      #todo
    if opInt == 169: #LDA immediate
      #loads the hex value given as output to
      #the value given
      print(firstValueByte)
      self.pc += 2
      self.a = firstValueByte
    if opInt == 234: #NOP impl
      #increment program counter
      self.pc += 1

  def start(self):
    memoryInt = list(open(self.memoryFile, "rb").read())
    memoryHex = [hex(b) for b in memoryInt]
    while True:
      try:
        returnCode = self.executeInstruction(memoryHex[self.pc])
      except Exception as e:
        print("TERMINAL ERROR")
        print("*********")
        subprocess.run(["afplay", "err.mp3"])
        raise e
      if returnCode == "brk":
        print("PROGRAM ENDED")
        break
    self.Memory.memoryDisplayer(self)
