start:
    LDX #$00 ;loads the initial value
    LDA #$05 ;clears the zero flag and prints start character
    STA $D012 ;prints it
loop: ;main loop
    LDA $FF,X ;load the register at the highest zpg for 00
    STA $D012 ;print char
    INX ;go up by one
    CPX #$40 ;  if equal 64 = the end
    BEQ #06 ;if this is equal, jump up 6 to end!
    JMP !loop ;otherwise, this is reached and rejump to loop
end:
    JMP !start ;restart from the beginning
