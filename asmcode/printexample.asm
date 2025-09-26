JMP !start
printXChar:
    TXA
    STA $D012
    RTS
start:
    LDX #02
    JSR !printXChar
    BRK
