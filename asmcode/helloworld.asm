start:
    JMP !loop
loop:
    INX
    TXA
    STA $D012
    CMP #3E
    BEQ #05
    NOP
    JMP !loop
end:
    JMP !start
