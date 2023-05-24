# Author: Rosita Aguirre Plascencia & Damian López Virgen
# Subject: Compilers
# Id: 0225352 & 0225228

# Compiler Project

# Run:     python .\main.py <file name> <output file name>
# Example: python .\main.py .\Tests_0 .\Tests_0_out.txt
# Example: python .\main.py .\ArchivoPrueba.up .\ArchivoPrueba.lex

import sys
from functions.lexFunctions import *
from functions.stateFunctions import *


lexemas  = []
separate = []

# *************** MAIN ***************

# Gets input and output file's names
file = "Tests_0" #Tests_0" #sys.argv[1]
fileOutput = sys.argv[2] if len(sys.argv) == 3 else "Tests_0.lex"

# File to read
with open(file, "r") as f:
	identifier   = ""
	tempElmt     = ""
	tempLexm     = []
	skipNext     = 0
	alfaOpen     = False
	comtOpen     = False

	# To analyze each character of each line on the file
	for i,l in enumerate(f):
		i += 1
		delimiters = ".,;()[]:\"+-*/%^=>< \n\t"
		separate.extend(split_with_delimiters(l, delimiters,i))

	for i,e in enumerate(separate):
		if skipNext == 0:
			if comtOpen:					# Skips elements while are in the line of a comment
				if e[0] == "\n":				# (unit new line)
					comtOpen =  False
			else:
				if alfaOpen:				# Add elements if an alfanumeric value is open open " / close ""
					tempElmt += e[0]
					if e[0] == "\"":
						lexemas.append([tempElmt, keysList[9], e[1]])     					# Add CteAlfa to lexemas
						tokens["<CteAlfa>"].add(tempElmt)           					# Add CteAlfa to the set
						alfaOpen = False
				else:
					if not isSpace(e[0]):
						token = clsfLex(e[0])
						if token != -1:
							if e[0] in ":=></": # Checks compose lexema
								if i+1 < len(separate) and separate[i+1][0] in ":=></":
									if (e[0] == "/" and separate[i+1][0] == "/"):            # Checks if is a comment the following line
										comtOpen =  True
									else:
										tempElmt = e[0] + separate[i+1][0]
										token = clsfLex(tempElmt)
										lexemas.append([tempElmt, token, e[1]])
										skipNext = 1
								else:
									lexemas.append([e[0], token, e[1]])
							else:
								#if token != keysList[6]: # Identifier just once ?
								lexemas.append([e[0], token, e[1]])
								if isTokenIdentifier(token,e[0]):
									identifier = e[0]
								
						else: 										# Checks if is an identifier or a value
							if e[0] == "\"":												# alfanumeric value -> CteAlfa
								tempElmt = e[0]
								alfaOpen = True

							elif e[0] in {"verdadero", "falso"}:        					# bool value -> CteLog
								lexemas.append([e[0], keysList[10], e[1]])   					# Add CteLog to lexemas
								tokens["<CteLog>"].add(e[0])          						# Add CteLog to the set
							
							elif isNumeric(e[0]):
								if i+2 < len(separate) and (separate[i+1][0] == "."):
									if isNumeric(separate[i+2][0]):						# decimal value -> CteReal
										tempElmt = e[0] + "." + separate[i+2][0]
										lexemas.append([tempElmt, keysList[8], e[1]])    		# Add CteReal to lexemas
										tokens["<CteReal>"].add(tempElmt)          		# Add CteReal to the set
										skipNext = 2
								else:													# integer value -> CteEnt
									lexemas.append([e[0], keysList[7], e[1]])  					# Add CteEnt to lexemas
									tokens["<CteEnt>"].add(e[0])          					# Add CteEnt to the set

							elif identifier != "": 
								lexemas.append([e[0], keysList[6], e[1]])  						# Add identifier to lexemas
								tokens["<Ident>"].add(e[0])            					# Add identifier to the set
								if not (identifier in {"variables", "constantes"}):
									identifier = ""
							else:
								lexemas.append([e[0], keysList[6], e[1]])
								tokens["<Ident>"].add(e[0])
		else:
			skipNext-=1

#New file to write the content without spaces
with open(fileOutput, "w+") as nf:
   
    nf.write(("{:<30}|{}\n").format('Lexema', 'Token'))
    header = "--------------------------------------------\n"
    nf.write(header)
    [nf.write(("{:<30}|{}\n").format(l[0], l[1])) for l in lexemas]
    
# Review Grammar
if checkGrammar(lexemas) == 1:
	print("\nCompile with success!\n")
else:
	print("\nThere's an error in your code :'(\n")


# programa
# 	si (1 = 2) hacer limpias;
#   a:=3;
# fin de programa


# programa
# 	variables a: entero;
# fin de programa