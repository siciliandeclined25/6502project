**6502 Processor**

This is a pet project to make a fully functional 6502 instruction set and hardware emulation for an Apple 1 (eventually) in Python3.

**What's the point?**

I want to do something and work on a project in EECS 169 so this is it

**What works?**
This last recent commit was a major rewrite. 
Now there is a working memory file where 6502 is stored (roughly 4K of ram) such as an Apple 1 of the era would be. Not only that, but there is an integrated 6502 compilier that is able to take nameespaces and convert them to valid 6502.

This means that several functions must be rewritten from scratch. Working so far are the simple

NOP impl
BRK impl
LDA imm

I hope to add more exec codes soon


**What's the end goal again?**
To run wozmod and maybe even Apple 1 basic as was run once on Apple machines. This could be a really cool (slow) way to emulate on less capable machines that run Python.

