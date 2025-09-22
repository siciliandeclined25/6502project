import subprocess
import time
class SixFiveOTwo:
  def __init__(self, file="mem.b", size=0x1000):
    self.memoryFile = file
    data = bytes(size) #fill full of empty 0s
    with open(self.memoryFile, "wb") as f:
         f.write(data)
    self.displayCommandAfter = False
    #my own homemade 6502 optable!
    self.optable = {
    "BRK impl": {"ascii": "BRK", "bytes": 00, "space": 1},
    "NOP impl": {"ascii": "NOP", "bytes": 0xEA,  "space": 1},
    "LDA zpg": {"ascii": "LDA", "bytes": 0xA5,  "space": 2}, #zeropage (0-256)
    "LDA imm": {"ascii": "LDA", "bytes": 0xA9,  "space": 2}, #LDA immediate (just load hex value into accumulator
    "LDA zpg x": {"ascii": "LDA", "bytes": 0xB5,  "space": 2},
    "LDX imm": {"ascii": "LDA", "bytes": 0xA2,  "space": 2},
    "LDA abs": {"ascii": "LDA", "bytes": 0x01},
    "STA zpg": {"ascii": "STA", "bytes": 0x65,  "space": 2},
    "STA abs": {"ascii": "STA", "bytes": 0x8D,  "space": 2},
    "INX imm": {"ascii": "INX", "bytes": 0xE8,  "space": 2},
    "DEX imm": {"ascii": "DEX", "bytes": 0xCA,  "space": 2},
    "JMP imm": {"ascii": "JMP", "bytes": 0x4C,  "space": 2},
    "CMP imm": {"ascii": "CMP", "bytes": 0xC9,  "space": 2},
    "BCC rel": {"ascii": "BCC", "bytes": 0x90,  "space": 2},
    "BEQ rel": {"ascii": "BEQ", "bytes": 0xF0,  "space": 2},
    "BPL rel": {"ascii": "BPL", "bytes": 0x10,  "space": 3},
    "CLC impl": {"ascii": "CLC", "bytes": 0x18,  "space": 1},
    "CPX imm": {"ascii": "CPX", "bytes": 0xE0,  "space": 2},
    "JSR abs": {"ascii": "JSR", "bytes": 0x20,  "space": 3},
    "RTS impl": {"ascii": "RTS", "bytes": 0x60,  "space": 1},

    }
    self.characters = [
        " ", "!", '"', "#", "$", "%", "&", "'", "(", ")", "*", "+", ",", "-", ".", "/",
        "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", ":", ";", "<", "=", ">", "?",
        "@", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O",
        "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "[", "\\", "]", "^", "_"
    ]

    #6502 memory variables!!!
    self.a = 0
    self.x = 0
    self.y = 0
    self.pc = 0 #program counter
    self.sp = 0xFF #stack pointer
    self.nextPCIncrement = 0
    self.carryFlag = 0
    self.zeroFlag = 0
    self.negFlag = 0
  def getB(self, byteLocation):
      memoryInt = list(open(self.memoryFile, "rb").read())
      return memoryInt[byteLocation]
  def setB(self, byteLocation, byteValue):
      #(special case are special enough to break the rules)
      #(when it's 50 year old hardware emulation)
      if int(byteLocation) == 53266: #decimal reprsentation of D012
        print(str(self.characters[self.a]), end="", flush=True)
        return False
      memoryInt = list(open(self.memoryFile, "rb").read())
      memoryInt[byteLocation] = byteValue
      open(self.memoryFile, "wb").write(bytes(memoryInt))
  def convertLittleEndian(self, integer):
      lowByte = (integer >> 8) & 0xFF   # top 8 bits
      highByte  = integer & 0xFF           # bottom 8 bits
      return highByte, lowByte
  def memoryDisplayer(self):
      print("MEMORY")
      memoryInt = list(open(self.memoryFile, "rb").read())
      i = 0
      while True:
        opcodevalue = "NONE"
        for values in self.optable.items():
            if values[1]["bytes"] == memoryInt[i]:
                opcodevalue = values[1]['ascii']
        print("ADDR: " + str(hex(i)) + " | VALUE: " + str(hex(memoryInt[i])) + "| IN DEC: " + str(int(memoryInt[i] )) + " | OPCODE: " + opcodevalue)
        userPrompt = input("(G)oto addr (S)tack (I)nternal Variables (B)ig View (C)hange value (Q)uit").lower()
        if userPrompt == "q":
          break
        if userPrompt == "b":
            print(memoryInt)
        if userPrompt == "s":
            for addr in range(0x0100, 0x0200):
                print(f"${addr:04X}: {memoryInt[addr]:02X}")
        if userPrompt == "i":
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
    labelsGiven = []
    print("CONVERTING....")
    while True:
      if len(fileToConvert) == byteLocation:
          break
      currentByte = fileToConvert[byteLocation]
      print(".", end="")
      try: #if this fails then it's just empty space
          trueKeyword = currentByte.split(";")[0].split()[0]
      except IndexError:
          byteLocation += 1
          continue
      try:
        trueByteValue = currentByte.split()[1]

      except IndexError: #no keyword
        trueByteValue = ""
      if trueKeyword[-1] == ":": #label, so jump to the correct value
          labelsGiven.append({"name": trueKeyword[:-1], "location": len(bytesGiven)})
          bytesGiven.append(self.optable["NOP impl"]["bytes"])#this is added so that when
          #it jumps to this memory location it's not empty and still exists on a 1:1 ratio
      #BRK convert
      if trueKeyword == "BRK":
        bytesGiven.append(self.optable["BRK impl"]["bytes"])
      elif trueKeyword == "CPX":
        if trueByteValue[0] == "#":#immediate
            bytesGiven.append(self.optable["CPX imm"]["bytes"])
            bytesGiven.append(int(trueByteValue.replace("#", "").replace("$", ""), 16))
      elif trueKeyword == "NOP":
        bytesGiven.append(self.optable["NOP impl"]["bytes"])
      elif trueKeyword == "BCC":
        bytesGiven.append(self.optable["BCC rel"]["bytes"])
      elif trueKeyword == "DEX":
          bytesGiven.append(self.optable["DEX imm"]["bytes"])
      elif trueKeyword == "CMP":
          if trueByteValue[0] == "#":
              bytesGiven.append(self.optable["CMP imm"]["bytes"])
              bytesGiven.append(int(trueByteValue.replace("#", "").replace("$", ""), 16))
      elif trueKeyword == "JMP":
          if trueByteValue[0] == "$":
            bytesGiven.append(self.optable["JMP imm"]["bytes"])
            twoByteAdd = int(trueByteValue.replace("#", "").replace("$", ""), 16)
            high, low = self.convertLittleEndian(twoByteAdd)
            bytesGiven.append(high) #add both extra
            bytesGiven.append(low)
          if trueByteValue[0] == "!":
              bytesGiven.append(self.optable["JMP imm"]["bytes"])
              foundLabel = False
              for labelReference in labelsGiven:
                  if labelReference["name"] == trueByteValue.replace("!", ""):
                      print("!", end="")
                      #remember that we have to divide this between low/high bytes
                      twoByteAdd = labelReference["location"]
                      highByte, lowByte = self.convertLittleEndian(twoByteAdd)
                      #now we can add the label to the correct place
                      bytesGiven.append(highByte)
                      bytesGiven.append(lowByte)
                      foundLabel = True
              if not foundLabel:
                  #we cannot find this label, so let's cross our fingers and just hope that the label exists later
                  labelsGiven.append({"name": trueByteValue.replace("!", ""), "location": False})
                  bytesGiven.append("ref!" + trueByteValue.replace("!", ""))
      elif trueKeyword == "INX":
          bytesGiven.append(self.optable["INX imm"]["bytes"])
      elif trueKeyword == "CLC":
          bytesGiven.append(self.optable["CLC impl"]["bytes"])
      elif trueKeyword == "BEQ":
          bytesGiven.append(self.optable["BEQ rel"]["bytes"])
          try:
              bytesGiven.append(int(trueByteValue.replace("#", "")))
          except ValueError:
              bytesGiven.append("ref!" + trueByteValue.replace("#", ""))
      elif trueKeyword == "BPL":
          bytesGiven.append(self.optable["BEQ rel"]["bytes"])
          try:
              bytesGiven.append(int(trueByteValue.replace("#", "")))
          except ValueError:
              bytesGiven.append("ref!" + trueByteValue.replace("#", ""))
      elif trueKeyword == "RTS":
          bytesGiven.append(self.optable["RTS impl"]["bytes"])
      elif trueKeyword == "STA":
          if len(trueByteValue.replace("#", "")) <= 2:
              #zeropage addressing value is between 00 and FF
              bytesGiven.append(self.optable["STA zpg"]["bytes"])
              bytesGiven.append(int(trueByteValue.replace("#", ""), 16))
          else:
              #let's assume this is an absolute because no x or y and direct address
              bytesGiven.append(self.optable["STA abs"]["bytes"])
              twoByteAdd = int(trueByteValue.replace("#", "").replace("$", ""), 16)
              highByte, lowByte = self.convertLittleEndian(twoByteAdd)
              bytesGiven.append(highByte) #add both extra
              bytesGiven.append(lowByte)
      elif trueKeyword == "LDX":
          if trueByteValue[0] == "#": #immediate addressing
            bytesGiven.append(self.optable["LDX imm"]["bytes"])
            bytesGiven.append(int(trueByteValue.replace("$", "").replace("#", ""), 16))
      elif trueKeyword == "JSR":
          if trueByteValue[0] == "!":
              bytesGiven.append(self.optable["JSR abs"]["bytes"])
              foundLabel = False
              for labelReference in labelsGiven:
                  if labelReference["name"] == trueByteValue.replace("!", ""):
                      print("!", end="")
                      #remember that we have to divide this between low/high bytes
                      twoByteAdd = labelReference["location"]
                      highByte, lowByte = self.convertLittleEndian(twoByteAdd)
                      #now we can add the label to the correct place
                      bytesGiven.append(highByte)
                      bytesGiven.append(lowByte)
                      foundLabel = True
              if not foundLabel:
                  #we cannot find this label, so let's cross our fingers and just hope that the label exists later
                  labelsGiven.append({"name": trueByteValue.replace("!", ""), "location": False})
                  bytesGiven.append("ref!" + trueByteValue.replace("!", ""))
                  print("\nWARNING: Could not find label location for (" + str(trueByteValue.replace("!", "")) + "). Hoping all is good")
          else:
            bytesGiven.append(self.optable["JSR abs"]["bytes"])
            twoByteAdd = int(trueByteValue.replace("#", "").replace("$", ""), 16)
            highByte, lowByte = self.convertLittleEndian(twoByteAdd)
            bytesGiven.append(highByte) #add both extra
            bytesGiven.append(lowByte)

      elif trueKeyword == "LDA":
        if trueByteValue[0] == "$":
            if trueByteValue.replace("\n", "")[-1] == "X": #LDAzpgx
                bytesGiven.append(self.optable["LDA zpg x"]["bytes"])
                bytesGiven.append(int(trueByteValue.replace("$", "").split(",")[0], 16))
            #this means it must be memory at $
            if len(trueByteValue.replace("$", "")) <= 2:
                #zeropage addressing!
                bytesGiven.append(self.optable["LDA zpg"]["bytes"])
                #adds the current byte value
                bytesGiven.append(int(trueByteValue[1:]))
                #increment by two
        if trueByteValue[0] == "#":
          #this is immediate addressing
          #which means the value is
          #being loaded itself into the hex
          bytesGiven.append(self.optable["LDA imm"]["bytes"])
          #adds the current byte value
          bytesGiven.append(int(trueByteValue[2:], 16))
          #increment by two
          #
      #THE ALL IMPORTANT LINE TO INC BYTES
      byteLocation += 1
    #this is to add the remaining memory addresses
    bytesGiven += [0] * (4096 - len(bytesGiven))
    #now that we've iterated through all labels let's check to
    # make sure there are none that were referenced but
    # never given proper memory addresses

    # this descriptive variable basically adds an offset
    # each time an immediate value is added as a label
    # when referencing the object defined postlabel defined
    globalFixPointerFromImmediateOffset = 0
    skipImmediateOffset = False
    for pointer,byteIn in enumerate(bytesGiven):
        if skipImmediateOffset:
            continue #this will skip so we don't read the bumped up label as a reference
        if "ref" in str(byteIn):
            #we found a reference, let's see if there
            # exists a corresponding value in the
            # names directory for the labels
            # pref = possible refrence
            for pref in enumerate(labelsGiven):
                if str(pref[1]["name"]) == byteIn.replace("ref!","") and pref[1]["location"] != False:#if this is assigned
                    #the added fix pointer from immediate offset basically fixes the
                    # problem by adding an extra integer to account for the offset of immediate memory addressing
                    # using JMP or labels which should always be assumed. not optimized but
                    # defintely is valid 6502
                    globalFixPointerFromImmediateOffset += 1
                    twoByteAdd = pref[1]["location"] + globalFixPointerFromImmediateOffset
                    lowByte = (twoByteAdd >> 8) & 0xFF   # top 8 bits
                    highByte  = twoByteAdd & 0xFF           # bottom 8 bits
                    bytesGiven[pointer] = highByte
                    bytesGiven.insert(pointer+1, lowByte) #insert it in!!! ;)

                    skipImmediateOffset = True #skips the next time so that we don't read the bumped value
    # finally check for straggles and fail if there
    # is no pointer for a label like ever bro
    counterByteErrLabel = 0
    for byte in bytesGiven:
        counterByteErrLabel += 1
        if "ref" in str(byte):
            print("ERR: unassigned label! -- " + str(counterByteErrLabel) + " "+ str(byte))
            raise MemoryError
    open(self.memoryFile, "wb").write(bytes(bytesGiven))
    memoryInt = list(open(self.memoryFile, "rb").read())
    nums = memoryInt[:30]
    hex_list = [hex(n) for n in nums]
    programList = []
    for value in hex_list:
        foundOpCode = False
        for opcode, opcodevalues in self.optable.items():
           ## print(opcodevalues["bytes"])
            ##print(type(opcodevalues["bytes"]))
           ## print(int(str(value), 16))
           ## print(type(int(value, 16)))
            if opcodevalues["bytes"] == int(str(value), 16):
                programList.append(opcode + " - " + str(value))
                foundOpCode = True
        if not foundOpCode:
            programList.append(str(value) + " - no op code")
    print("")
    for _ in programList: print (_)
    print("MEMORY WRITTEN")
    input("ready>")
    print("-------------")
  def executeInstruction(self, opCodeToexecute):
    opInt = int(opCodeToexecute, 16)
    firstValueByte = self.getB(self.pc+1)
    secondValueByte = self.getB(self.pc+2)
    time.sleep(0.005)
    result = -1
    if self.displayCommandAfter == True:
        pass
    if opInt == 0: #BRK impl
      #increment program counter
      self.pc += 1
      return "brk"
    if opInt == 164: #LDA zpg
      self.pc += 2 #two offset for value
      self.a = self.getB(self.pc+1)
      result = self.a
    if opInt == 0x18: #CLC
        self.carryFlag = 0
        self.pc += 1
    if opInt == 169: #LDA immediate
      #loads the hex value given as output to
      #the value given
      self.pc += 2
      self.a = firstValueByte
      result = self.a
    if opInt == 0xE0: #CPX immediate
        if self.x == firstValueByte: #if equal zeroflag true
            self.zeroFlag = 1
        if self.x >= firstValueByte: #if greater carry flag tru
            self.carryFlag = 1
        if self.x <= firstValueByte: #if lesser carry flag false
            self.carryFlag = 0
        invertedX = self.x #invertx
        invertedX &= 0xFF
        operand = firstValueByte #invertop
        operand &= 0xFF
        resultNFlag = (invertedX - operand) & 0xFF
        self.negativeFlag = (resultNFlag & 0x80) != 0 #negative flag
        self.pc += 2
    if opInt == 0x60: #RTS impl
        highByte = self.getB(self.sp+1)
        lowByte = self.getB(self.sp+2)
        finalByte = (lowByte << 8) | highByte
        self.pc = finalByte #get the value from the stack pointer and se it to the pc value
        self.sp += 2 #move it up by one because subroutines wooo
    if opInt == 165: #LDA immediate
        #loads the hex value given as output to
        #the value given
        self.pc += 2
        self.a = self.getB(firstValueByte)
        result = self.a
    if opInt == 0xB5: #LDA X
        self.pc += 2
        self.a = self.getB(firstValueByte) + self.x
        result = self.a
    if opInt == 0xC9:
        if self.a == firstValueByte:
            self.zeroFlag = 1
        self.pc += 2
    if opInt == 0x90:
        if self.carryFlag == 1:
            self.pc += firstValueByte
        else:
            self.pc += 2
    if opInt == 0xCA: #DEX
        self.x -= 1 if self.x != 0 else 0
        self.pc += 1
        result = self.x
    if opInt == 0xE8: #INX
        self.x +=  1 if self.x != 255 else 255
        self.pc += 1
        result = self.x
    if opInt == 0x4C: #JMP abs
        highByte = self.getB(self.pc+1)
        lowByte = self.getB(self.pc+2)
        finalByte = (lowByte << 8) | highByte
        self.pc = finalByte
    if opInt == 101: #STA zpg
        #loads into value the zeropage
        self.pc += 2
        self.setB(firstValueByte, self.a)
        result = self.a
    if opInt == 0xF0:
        if self.zeroFlag == 1:
            self.pc += int(str(firstValueByte), 0)
            self.displayCommandAfter = False
        else:
            self.pc += 2
    if opInt == 0xF0:
        if self.negativeFlag == 0:
            self.pc += int(str(firstValueByte), 0)
            self.displayCommandAfter = False
        else:
            self.pc += 2
    if opInt == 0x20: #JSR
        #for A, read the big comment below
        highByteJSRAddress = self.getB(self.pc+1)
        lowByteJSRAddress = self.getB(self.pc+2)
        #for B, ditto
        # gross gross gross it's the pc + 3 because that's the return address
        returnAddressForRT = self.pc + 3 #the expression space between the namespace and the two bit address
        ########
        # TO CLARIFY
        # this function does two things:
            # A. jump to the address that is given by the following two bit endian in
            # highByteJSRAddress/low. this is then converted and the program counter jumps
            # B. make a two bit endian reference value that is jumped to once RTS is called and recalled
        #i understand why this is what it is. it makes sense for the 6502 to be able to create JSR from
        # a non-tools perspective. BUT JMP does the same thing, where lables can just assign the value. so no.
        # i don't think this is useful. but this isn't 6502 how i like it. so let's go stack pointer!!!! :()
        newHighByte = (returnAddressForRT >> 8) & 0xFF
        newLowByte = returnAddressForRT & 0xFF
        #HIGH, LOW so that when it gets accessed it's read
        # like a little endian instead of a big
        # ex of a messup: 00 06 == 1356 or somebs because it's
        # assembled 06 00
        # now we go into this cursed deincrementation of the sp
        self.setB(self.sp, newHighByte)
        self.sp -= 1
        self.setB(self.sp, newLowByte)
        self.sp -= 1 #de novo
        #now we need to set the pc to be equal to the JSR address
        self.pc =  (lowByteJSRAddress << 8) | highByteJSRAddress

    if opInt == 141: #STA abs
        #loads into value the zeropage
        highByte = self.getB(self.pc+1)
        lowByte = self.getB(self.pc+2)
        finalByte = (lowByte << 8) | highByte
        self.setB(finalByte, self.a)
        self.pc += 3
        result = self.a
    if opInt == 0xA2:
        self.x = firstValueByte
        self.pc += 2
        result = self.x
    if opInt == 234: #NOP impl
      #increment program counter
      self.pc += 1
  #ENDING RESULT BEHAVIOR CHANGES
    if result == 0:
      self.zeroFlag = 1
    elif result == -1:
        pass #nochange, result doesn't matter
    else:
        self.zeroFlag = 0 #this means that the zeroflag was cleared
  def start(self):
    memoryInt = list(open(self.memoryFile, "rb").read())
    memoryHex = [hex(b) for b in memoryInt]
    while True:
      try:
        returnCode = self.executeInstruction(memoryHex[self.pc])
      except Exception as e:
        print("TERMINAL ERROR")
        print("*********")
        #subprocess.Popen(["afplay", "err.mp3"])
        if input("do you wanna see the err> ") == "y":
            raise e
        self.memoryDisplayer()
      if returnCode == "brk":
        print("\n-------------")
        print("PROGRAM ENDED")
        break
    self.memoryDisplayer()
