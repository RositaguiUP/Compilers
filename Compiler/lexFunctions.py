from variables import *


# *************** FUNCTIONS ***************

# Function to check if a character is a number by its ASCII
# Input: value to check
# Output: boolean, true if is numeric, false if not
def isNumeric(val):
	for d in val:
		if not (ord(d) >= 48 and ord(d) <= 57):
			return False
	return True

# Function to check if a character is a space
# Input: value of the character to check
# Output: boolean, true if is a space, false if not
def isSpace(val):
	return (val == ' ' or val == "\t" or val == "\n")

# Function to check if is any token
# Input: value to check
# Output: the token key if is part of any, -1 if not
def clsfLex(lex):
	clsf = -1
	for t in keysList:
		if lex in tokens[t]:
			clsf = t
			break
	return clsf

# Function to split a string by defined delimeters
# Input: string to split, delimeters
# Output: list with all the elements of the splitted string
def split_with_delimiters(text, delimiters):
    parts = []
    current_part = ""
    for char in text:
        if char in delimiters:
            if current_part:
                parts.append(current_part)
            parts.append(char)
            current_part = ""
        else:
            current_part += char
    if current_part:
        parts.append(current_part)
    return parts

# Function to check if the element is an identifier
# Input: actual token of the element, element
# Output: boolean, true if is an identifier, false if not
def isTokenIdentifier(token, e):
	if token == keysList[4]: 			# PalRes
		return (e in {"funcion", "procedimiento", "variables", "constantes"})
	return False
