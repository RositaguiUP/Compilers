
# *************** VARIABLES ***************

tokens = {
	"<Delim>":   set([".", ",", ";", "(", ")", "[", "]", ":", "\n", "\t"]),    #0 
	"<OpArit>":  set(["+", "-", "*", "/", "%", "^"]),                          #1
	"<OpRel>":   set(["=", "<>", "<", ">", "<=", ">="]),                       #2 
	"<OpLog>":   set(["y", "o", "no"]),                                  	   #3
	"<PalRes>":  set(["constantes", "variables", "real", "alfanumerico",
		   		"logico", "entero", "funcion", "inicio", "fin", "de", 
				"procedimiento", "regresa", "si", "hacer", "sino", "cuando",
				"el", "valor", "sea", "otro", "desde", "hasta", "incr",
				"decr", "repetir", "que", "mientras", "se", "cumpla",
				"continua", "interrumpe", "limpia","lee", "imprime",
				"imprimeln", "verdadero", "falso"]),                           #4
	"<OpAsig>":  set([":="]),    #5
	"<Ident>":   set(),          #6
	"<CteEnt>":  set(),          #7
	"<CteReal>": set(),          #8
	"<CteAlfa>": set(),          #9
	"<CteLog>":  set(),          #10
	}

keysList = list(tokens.keys())




# gramsList = []
# gramsList.append(Exprlog)
# gramsList.append(estatuto)
# gramsList.append(si)


# Exprlog  = [keysList[7], keysList[2], keysList[7]]
# estatuto = ["x"]
# si       = ["si", "(", Exprlog, ")", "hacer", estatuto]

# grams = {
# 	"Exprlog":  Exprlog,
# 	"estatuto": estatuto,
# 	"si":       si
# }


Exprlog  = [("t", keysList[7]), ("t", keysList[2]), ("t", keysList[7])]
estatuto = ["x"]
si       = ["si", "(", ("g", "Exprlog"), ")", "hacer"]

grams = {
	"Exprlog":  Exprlog,
	"estatuto": estatuto,
	"si":       si
}


gramsKeysList = list(grams.keys())

class State:
	def __init__(self, gram, pid, id):
		self.gram = gram
		self.parentId = pid
		self.id = id
		self.index = 0
		self.substates = []
		self.substateStart = False
	
	def addIndex(self):
		self.index += 1