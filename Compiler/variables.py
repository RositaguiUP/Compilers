
# *************** Tokens ***************
tokens = {
	"<Delim>":   set([".", ",", ";", "(", ")", "[", "]", ":", "\n", "\t"]),    #0 
	"<OpArit>":  set(["+", "-", "*", "/", "%", "^"]),                          #1
	"<OpRel>":   set(["=", "<>", "<", ">", "<=", ">="]),                       #2 
	"<OpLog>":   set(["y", "o", "no"]),                                  	   #3
	"<PalRes>":  set(["programa", "constantes", "variables", "real", "alfanumerico",
		   		"logico", "entero", "funcion", "inicio", "fin", "de", 
				"procedimiento", "regresa", "si", "hacer", "sino", "cuando",
				"el", "valor", "sea", "otro", "desde", "hasta", "incr",
				"decr", "repetir", "que", "mientras", "se", "cumpla",
				"continua", "interrumpe", "limpia","lee", "imprime",
				"imprimeln"]),                           #4
	"<OpAsig>":  set([":="]),    #5
	"<Ident>":   set(),          #6
	"<CteEnt>":  set(),          #7
	"<CteReal>": set(),          #8
	"<CteAlfa>": set(),          #9
	"<CteLog>":  set(["verdadero", "falso"]),      	    #10
	}

keysList = list(tokens.keys())

# *************** Aux Grammar Rules ***************

# t  -> token
# g  -> grammar
# cg -> compound grammar
# |  -> or

# e  -> could be empty
# ne -> could'nt be empty

# *************** Grammar Rules ***************
Prgrm 			= [("g", "e", "constantes"), ("g", "e", "variables"), ("g", "e", "ProtFuncProc"), ("g", "e", "FuncProc"),							# Revisar constantes
	     			"programa", ("g", "e", "Block"), "fin", "de", "programa"]
# Vars
constantes 		= ["constantes", ("g", "ne", "GpoConst")]
variables 		= ["variables", ("g", "ne", "GpoVars")]
GpoVars 		= [("g", "ne", "GpoIds"), ":", ("g", "ne", "tipo"), ";", ("g", "e", "GpoVars")]
GpoIds 			= [("t", "ne", keysList[6]), ("g", "e", "Dimens"), ("cg", "e", ":=", ("|", "ne", ("t", "ne", keysList[7]),
					("t", "ne", keysList[6]))), ("cg", "e", ",", ("g", "e", "GpoIds"))]
Dimens 			= ["[", ("|", "ne", ("t", "ne", keysList[7]), ("t", "ne", keysList[6])), "]", ("g", "e", "Dimens")]
tipo 			= [("|", "ne", "entero", "real", "alfabetico", "logico")]
# Func
ProtFuncProc 	= [("|", "ne", ("g", "ne", "ProtFunc"), ("cg", "ne", ("g", "ne", "ProtProc"), ("g", "e", "ProtFuncProc")))]
ProtFunc 		= ["funcion", ("g", "ne", ("t", "ne", keysList[6])), "(", ("g", "ne", "Params"), ")", ":", ("g", "ne", "tipo"), ";"]
ProtProc 		= ["procedimiento", ("g", "ne", ("t", "ne", keysList[6])), "(", ("g", "ne", "Params"), ")", ";"]
Params 			= [("g", "ne", "GpoPars"), ":", ("g", "ne", "tipo"), ("cg", "e", ";", ("g", "ne", "Params"))]
GpoPars 		= [("t", "ne", keysList[6]), ("cg", "e", ",", ("g", "ne", "GpoPars"))]
FuncProc 		= [("|", "ne", ("g", "ne", "procedimiento"), ("cg", "ne", ("g", "ne", "funcion"), ("g", "e", "FuncProc")))]
procedimiento 	= ["procedimiento", ("g", "ne", ("t", "ne", keysList[6])), "(", ("g", "e", "Params"), ")", ("g", "e", "variables"),
                   	"inicio", ("g", "e", "Block"), "fin", "de", "procedimiento", ";"]
funcion 		= ["funcion",  ("g", "ne", ("t", "ne", keysList[6])), "(", ("g", "e", "Params"), ")", ("g", "e", "variables"),
                   	"inicio", ("g", "e", "Block"), "fin", "de", "funcion", ";"]
# Statements
Block 			= [("g", "e", "estatuto"), ";", ("g", "e", "Block")]
estatuto 		= [("|", "ne", ("g", "ne", "si"), "limpia",  ("g", "ne", "desde"), ("g", "ne", "repetir"), ("g", "ne", "mientras"),
	       			("g", "ne", "cuando"), ("g", "ne", "regresa"), ("g", "ne", "asigna"), ("g", "ne", "lproc"),
					("g", "ne", "imprime"), ("g", "ne", "imprimenl"), ("g", "ne", "leer"), "interrumpe", "continua")]
si 				= ["si", "(", ("g", "ne", "Exprlog"), ")", "hacer", ("g", "e", "BckEsp"),
	  				("cg", "e", "sino", ("g", "e", "BckEsp"))]
BckEsp 			= [("|", "ne", ("g", "e", "estatuto"), ("cg", "ne", "inicio", ("g", "e", "Block"), "fin"))]
desde 			= ["desde", "el", "valor", "de", ("g", "ne", "asigna"), "hasta", ("g", "ne", "exp"),
             		("cg", "e", ("|", "ne", "inc", "decr"), ("c", "ne", ("t", "ne", keysList[7]))), ("g", "e", "BckEsp")]
repetir 		= ["repetir", ("g", "e", "Block"), "hasta", "que", "(", ("g", "ne", "Exprlog"), ")"]
mientras 		= ["mientras", "se", "cumpla", "que", "(", ("g", "ne", "Exprlog"), ")", ("g", "e", "BckEsp")]
asigna 			= [("t", "ne", keysList[6]), ("cg", "e", "[", ("g", "ne", "Udim"), "]"), ":=", ("g", "ne", "Exprlog")]
cuando 			= ["cuando", "el", "valor", "del", ("t", "ne", keysList[6]), "inicio", ("g", "ne", "GpoSea"), 
	     			"otro", ":", ("g", "e", "BckEsp"), "fin"]
GpoSea 			= ["sea", ("g", "ne", "GpoConst"), ":", ("g", "e", "BckEsp"), ("g", "e", "GpoSea")]
GpoConst 		= [("g", "ne", "cte"), ("g", "e", "GpoConst")]
Udim 			= [("g", "e", "Expr"), ("cg", "e", "[", ("g", "ne", "Udim"), "]")]
regresa 		= ["regresa", ("cg", "e", "(", ("g", "ne", "Exprlog"), ")")]
Exprlog 		= [("g", "ne", "Opy"), ("cg", "e", "o", ("g", "ne", "Exprlog"))]
# Operators
Opy 			= [("g", "ne", "Opno"), ("cg", "e", "y", ("g", "ne", "Opy"))]
Opno 			= ["[no", ("g", "ne", "Oprel")]
Oprel 			= [("g", "ne", "Expr"), ("cg", "e", ("t", "ne", keysList[2]), ("g", "ne", "Opy"))]
Expr 			= [("g", "ne", "Multi"), ("cg", "e", ("|", "ne", "+", "-"), ("g", "ne", "Expr"))]
Multi 			= [("g", "ne", "Expo"), ("cg", "e", ("|", "ne", "*", "/", "%"), ("g", "ne", "Multi"))]
Expo 			= [("g", "ne", "signo"), ("cg", "e", "^", ("g", "ne", "Expo"))]
signo 			= ["[-", ("g", "ne", "termino")]
termino 		= [("|", "ne",  ("cg", "ne", ("t", "ne", keysList[6]), ("cg", "e", "[", ("|", "ne", ("g", "ne", "lfunc"), ("g", "ne", "Udim") ,"]"))),
	      			("cg", "ne", "(", ("g", "ne", "Exprlog"), ")"), ("t", "ne", keysList[7]), 
					("t", "ne", keysList[8]),("t", "ne", keysList[9]), ("t", "ne", keysList[10]))] 
lproc 			= [("t", "ne", keysList[6]), "(", ("g", "e", "Uparams"), ")"]
lfunc 			= [("t", "ne", keysList[6]), "(", ("g", "e", "Uparams"), ")"]
imprime 		= ["imprime", "(", ("g", "e", "GpoExp"), ")"]
imprimenl 		= ["imprimenl", "(", ("g", "e", "GpoExp"), ")"]
GpoExp 			= [("g", "ne", "Exprlog"), ("cg", "e",  ",", ("g", "e", "GpoExp"))]
Uparams 			= [("g", "ne", "Exprlog"), ("cg", "e",  ",", ("g", "e", "Uparams"))]
leer 			= ["lee", "(", ("t", "ne", keysList[6]), ("cg", "e", "[", ("g", "ne", "Udim"), "]"), ")"]





grams = {
	"Prgrm": 			Prgrm,
	"constantes": 		constantes,
	"variables": 		variables,
	"GpoVars": 			GpoVars,
	"GpoIds": 			GpoIds,
	"Dimens": 			Dimens,
	"tipo": 			tipo,
	"ProtFuncProc": 	ProtFuncProc,
	"ProtFunc": 		ProtFunc,
	"ProtProc": 		ProtProc,
	"Params": 			Params,
	"GpoPars": 			GpoPars,
	"FuncProc": 		FuncProc,
	"procedimiento":	procedimiento,
	"funcion": 			funcion,
	"Block": 			Block,
	"estatuto": 		estatuto,
	"si":       		si,
	"BckEsp": 			BckEsp,
	"desde": 			desde,
	"repetir": 			repetir,
	"mientras": 		mientras,
	"asigna": 			asigna,
	"cuando": 			cuando,
	"GpoSea": 			GpoSea,
	"GpoConst": 		GpoConst,
	"Udim": 			Udim,
	"regresa": 			regresa,
	"Exprlog":  		Exprlog,
	"Opy":				Opy,
	"Opno": 			Opno,
	"Oprel": 			Oprel,
	"Expr": 			Expr,
	"Multi": 			Multi,
	"Expo": 			Expo,
	"signo": 			signo,
	"termino": 			termino,
	"lproc": 			lproc,
	"lfunc": 			lfunc,
	"imprime": 			imprime,
	"imprimenl": 		imprimenl,
	"GpoExp": 			GpoExp,
	"Uparams": 			Uparams,
	"leer": 			leer
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