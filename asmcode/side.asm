CLC
LDA $FF,X ;loads 00 into x
STA $D012 ; print char in ac
INX ; go up by 1
CMP #$3D ; compare to list length (61). if == set zeroflag
BEQ $#
JMP $0000 ;go set the pc back to 000
BRK ;end program
