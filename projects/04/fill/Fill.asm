// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.
	
(LOOP)	// loop start

	@tracker	//address tracker
	M=0
	
	@KBD
	D=M		// D=KBD
	@LOOP
	D;JEQ		// if KBD=0 goto WHITE
	@BLACK
	0;JEQ		// else goto BLACK
	
(WHITE)
	
	@tracker
	D=M		// D=tracker
	@SCREEN
	A=A+D		// D=@SCREEN + tracker
	M=0		// A=0, current screen
	@tracker
	M=M+1		// tracker++

	@8191
	D=A
	@tracker
	D=M-D		// D=M[i]-A[SCREENmax]
	@WHITE
	D;JLE		// if D<0 goto WHITE
	@LOOP
	0;JEQ		// else goto LOOP

(BLACK)

	@tracker
	D=M		// D=tracker
	@SCREEN
	A=A+D		// D=@SCREEN + tracker
	M=-1		// A=1, current screen
	@tracker
	M=M+1		// tracker++

	@8191
	D=A
	@tracker
	D=M-D		// D=M[i]-A[SCREENmax]
	@BLACK
	D;JLE		// if D<0 goto WHITE


	@tracker
	M=0		// reset to 0
	
(AFTERLOOP)
	
	@KBD
	D=M		// D=KBD
	@WHITE
	D;JEQ		// if KBD=0 goto WHITE
	@AFTERLOOP
	0;JEQ		// else goto AFTERLOOP
