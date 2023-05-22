# Author: Rosita Aguirre Plascencia & Damian López Virgen
# Subject: Compilers
# Id: 0225352 & 0225228

# Compiler Project

# Run:     python .\main.py <file name> <output file name>
# Example: python .\main.py .\Tests_0 .\Tests_0_out.txt
# Example: python .\main.py .\ArchivoPrueba.up .\ArchivoPrueba.lex

import sys
from lexFunctions import *
from stateFunctions import *


lexemas  = []
separate = []

# *************** MAIN ***************

# Gets input and output file's names
file = "practica.up" #Tests_0" #sys.argv[1]
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
								lexemas.append([e, keysList[6]])
								tokens["<Ident>"].add(e)
		else:
			skipNext-=1

#New file to write the content without spaces
with open(fileOutput, "w+") as nf:
    header = "----------------------------------------------\n\tLexema \t\tToken\n----------------------------------------------"
    nf.write(header)
    [nf.write("\n\t" + l[0] + "\t\t\t\t" + l[1]) for l in lexemas]
    
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