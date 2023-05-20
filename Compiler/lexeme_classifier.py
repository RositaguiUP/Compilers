# Author: Rosita Aguirre Plascencia
# Subject: Compilers
# Id: 0225352 

# Lexeme Classifier

# Run:     python .\lexeme_classifier.py <file name> <output file name>
# Example: python .\lexeme_classifier.py .\Tests_0 .\Tests_0_out.txt
# Example: python .\lexeme_classifier.py .\ArchivoPrueba.up .\ArchivoPrueba.lex

import sys

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

# *************** VARIABLES ***************

tokens = {
	"<Delim>":   set([".", ",", ";", "(", ")", "[", "]", ":", "\n", "\t"]),    #Together
	"<OpArit>":  set(["+", "-", "*", "/", "%", "^"]),                          #Together
	"<OpRel>":   set(["=", "<>", "<", ">", "<=", ">="]),                       #Together 
	"<OpLog>":   set(["y", "o", "no"]),                                  	   #Separate
	"<PalRes>":  set(["constantes", "variables", "real", "alfanumerico",
		   		"logico", "entero", "funcion", "inicio", "fin", "de", 
				"procedimiento", "regresa", "si", "hacer", "sino", "cuando",
				"el", "valor", "sea", "otro", "desde", "hasta", "incr",
				"decr", "repetir", "que", "mientras", "se", "cumpla",
				"continua", "interrumpe", "limpia","lee", "imprime",
				"imprimeln", "verdadero", "falso"]),                           #Separate
	"<OpAsig>":  set([":="]),                                                  #Together
	"<Ident>":   set(),
	"<CteEnt>":  set(),
	"<CteReal>": set(),
	"<CteAlfa>": set(),
	"<CteLog>":  set(),  
	}

keysList = list(tokens.keys())

lexemas  = []
separate = []

# *************** MAIN ***************

# Gets input and output file's names
file = sys.argv[1]
fileOutput = sys.argv[2] if len(sys.argv) == 3 else "output.lex"

# File to read
with open(file, "r") as f:
	identifier   = ""
	tempElmt     = ""
	tempLexm     = []
	skipNext     = 0
	alfaOpen     = False
	comtOpen     = False

	# To analyze each character of each line on the file
	for l in f:
		delimiters = ".,;()[]:\"+-*/%^=>< \n\t"
		separate.extend(split_with_delimiters(l, delimiters))

	for i,e in enumerate(separate):
		if skipNext == 0:
			if comtOpen:					# Skips elements while are in the line of a comment
				if e == "\n":				# (unit new line)
					comtOpen =  False
			else:
				if alfaOpen:				# Add elements if an alfanumeric value is open open " / close ""
					tempElmt += e
					if e == "\"":
						lexemas.append([tempElmt, keysList[9]])     					# Add CteAlfa to lexemas
						tokens["<CteAlfa>"].add(tempElmt)           					# Add CteAlfa to the set
						alfaOpen = False
				else:
					if not isSpace(e):
						token = clsfLex(e)
						if token != -1:
							if e in ":=></": # Checks compose lexema
								if i+1 < len(separate) and separate[i+1] in ":=></":
									if (e == "/" and separate[i+1] == "/"):            # Checks if is a comment the following line
										comtOpen =  True
									else:
										tempElmt = e + separate[i+1]
										token = clsfLex(tempElmt)
										lexemas.append([tempElmt, token])
										skipNext = 1
								else:
									lexemas.append([e, token])
							else:
								#if token != keysList[6]: # Identifier just once ?
								lexemas.append([e, token])
								if isTokenIdentifier(token,e):
									identifier = e
								
						else: 										# Checks if is an identifier or a value
							if e == "\"":												# alfanumeric value -> CteAlfa
								tempElmt = e
								alfaOpen = True

							elif e in {"verdadero", "falso"}:        					# bool value -> CteLog
								lexemas.append([e, keysList[10]])   					# Add CteLog to lexemas
								tokens["<CteLog>"].add(e)          						# Add CteLog to the set
							
							elif isNumeric(e):
								if i+2 < len(separate) and (separate[i+1] == "."):
									if isNumeric(separate[i+2]):						# decimal value -> CteReal
										tempElmt = e + "." + separate[i+2]
										lexemas.append([tempElmt, keysList[8]])    		# Add CteReal to lexemas
										tokens["<CteReal>"].add(tempElmt)          		# Add CteReal to the set
										skipNext = 2
								else:													# integer value -> CteEnt
									lexemas.append([e, keysList[7]])  					# Add CteEnt to lexemas
									tokens["<CteEnt>"].add(e)          					# Add CteEnt to the set

							elif identifier != "": 
								lexemas.append([e, keysList[6]])  						# Add identifier to lexemas
								tokens["<Ident>"].add(e)            					# Add identifier to the set
								if not (identifier in {"variables", "constantes"}):
									identifier = ""
		else:
			skipNext-=1

# New file to write the content without spaces
with open(fileOutput, "w+") as nf:
    header = "----------------------------------------------\n\tLexema \t\tToken\n----------------------------------------------"
    nf.write(header)
    [nf.write("\n\t" + l[0] + "\t\t\t\t" + l[1]) for l in lexemas]