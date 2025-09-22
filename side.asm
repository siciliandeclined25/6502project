

LDA #$0E
STA #$D012
JSR !esoteric
LDA #$A0
NOP
NOP
NOP
esoteric:
    LDA #$0F
    STA #$D012
    RTS
