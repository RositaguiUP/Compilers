# Author: Rosita Aguirre Plascencia
# Subject: Compilers
# Id: 0225352 

# Run:     python .\CleanWhitespaces.py <file name> <output file name>
# Example: python .\CleanWhitespaces.py .\Tests_0 .\Tests_0_out.txt

import sys

# Gets input and output file's names
file = sys.argv[1]
fileOutput = sys.argv[2] if len(sys.argv) == 3 else "output_file"

textLine = []
numbers  = []

# Function to check if a character is a number by its ASCII
# Input: value of the character to check
# Output: boolean, true if is numeric, false if not
def isNumeric(val):
	numAscii = ord(val)
	return (numAscii >= 48 and numAscii <= 57)

# File to read
with open(file, "r") as f:
	tempNum      = ""
	lastWasDigit = False

	# To analyze each character of each line on the file
	for l in f:
		for c in l:
			# Checks if the actual char is a number to add to the temporal number
			if isNumeric(c):
				lastWasDigit = True
				tempNum     += c
			elif c == "." and lastWasDigit: # Helps to detect decimal numbers
				tempNum  += c
			elif lastWasDigit: # Determinates the end of the temporal number. it is added to the list and restart
				numbers.append(tempNum)
				lastWasDigit = False
				tempNum      = ""

			if c != ' ' and c != "\t": # Add the char if it's not any kind of space (respect line breaks)
				textLine.append(c)
			
	if lastWasDigit: # Prevents to don't forget to add a number if it's the last char in the file
		numbers.append(tempNum)

	print(numbers)

# New file to write the content without spaces
with open(fileOutput, "w+") as nf:
    [nf.write(c) for c in textLine]