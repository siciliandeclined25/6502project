LDA #$05     ; Load 5 into A
CMP #$03     ; Compare A with 3 (sets flags)
BPL !yay ; Branch to Positive if result >= 0 (N = 0)
; execution continues here if result < 0
BRK
yay:
LDA #$01
STA $D012
