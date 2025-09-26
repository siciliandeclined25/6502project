start:
    JMP !loop
loop:
    INX
    TXA
    STA $D012
    CMP #3E
    BEQ #08
    NOP
    JMP !loop
end:
    LDX #00
    JMP !start
