LDA #$01      ; Load 1 into A
STA $0200     ; Store A into memory at $0200
LDA #$FF      ; Load 255 into A
STA $0201     ; Store A into memory at $0201
LDA #$0A      ; Load 10 into A
STA $0202     ; Store A into memory at $0202
LDA $0200     ; Load value from $0200 back into A
STA $0203     ; Store it into $0203 (copy)

