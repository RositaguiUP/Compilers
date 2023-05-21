
# *************** Tokens ***************

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

# Prgrm 			= ["[", ("<constantes>", "]", "[", "<variables>", "]", "[", "<ProtFuncProc>", "]", "<FuncProc>", "programa", "<Block>", "fin", "de", "programa")],
# variables 		= ["variables", "<GpoVars>"],
# GpoVars 		= ["<GpoIds>", ":", "<tipo>", ";", "[", "<GpoVars>", "]"],
# GpoIds 			= ["Id", "[", "<Dimens>", "]", "[", ":=", "CteEnt", "|", "Id", "]", ",", "<GpoIds>"],
# Dimens 			= ["[", "CteEnt", "|", "Id", "]", "<Dimens>"],
# tipo 			= ["entero", "|", "real", "|", "alfabetico", "|", "logico"],
# ProtFuncProc 	= ["<ProtFunc>", "|", "<ProtProc>", "[", "<ProtFuncProc>", "]"],
# ProtFunc 		= ["funcion", "Id", "(", "<Params>", ")", ":", "<tipo>", ";"],
# ProtProc 		= ["procedimiento", "Id", "(", "<Params>", ")", ";"],
# Params 			= ["<GpoPars>", ":", "<tipo>", ";", "<Params>"],
# GpoPars 		= ["Id", ",", "<GpoPars>"],
# FuncProc 		= ["<procedimiento>", "|", "<funcion>", "[", "<FuncProc>", "]"],
# procedimiento 	= ["procedimiento", "Id", "(", "<Params>", ")", "[", "<variables>", "]", "inicio", "<Block>", "fin", "de", "procedimiento", ";"],
# funcion 		= ["funcion", "Id", "(", "<Params>", ")", ":", "<tipo>", "[", "<variables>", "]", "inicio", "<Block>", "fin", "de", "funcion", ";"],
# desde 			= ["desde", "el", "valor", "de", "<asigna>", "hasta", "<exp>", "[", "inc", "|", "decr", "CteEnt", "]", "[", "<BckEsp>", "]"],
# repetir 		= ["repetir", "[", "<Block>", "]", "hasta", "que", "(", "<Exprlog>", ")"],
# mientras 		= ["mientras", "se", "cumpla", "que", "(", "<Exprlog>", ")", "[", "<BckEsp>", "]"],
# asigna 			= ["Id", "[", "<Udim>", "]", ":=", "<Exprlog>"],
# cuando 			= ["cuando", "el", "valor", "del", "Id", "inicio", "<GpoSea>", "[", "otro", ":", "[", "<BckEsp>", "]", "]", "fin"],
# GpoSea 			= ["sea", "<GpoConst>", ":", "[", "<BckEsp>", "]", "[", "<GpoSea>", "]"],
# GpoConst 		= ["<cte>", ",", "<GpoConst>"],
# Udim 			= ["[", "<Expr>", "]", "[", "<Udim>", "]"],
# regresa 		= ["regresa", "(", "<Exprlog>", ")"],
# Expr 			= ["<Multi>", "[", "+", "|", "-", "<Expr>", "]"],
# lproc 			= ["Id", "(", "<Uparams>", ")"],
# lfunc 			= ["Id", "(", "<Uparams>", ")"],
# imprime 		= ["imprime", "(", "<GpoExp>", ")"],
# imprimenl 		= ["imprimenl", "(", "<GpoExp>", ")"],
# GpoExp 			= ["<Exprlog>", "[", ",", "<GpoExp>", "]"],
# Uparams 		= ["<Explog>", "[", ",", "<Uparams>", "]"],
# impi 			= ["limpia"],
# leer 			= ["lee", "(", "Id", "[", "<Udim>", "]", ")"]






estatuto 		= [("|", "ne", ("g", "ne", "si"), "limpiar")] #,  ("g", "ne", "desde"), ("g", "ne", "repetir"),
	       			# ("g", "ne", "mientras"), ("g", "ne", "cuando"), ("g", "ne", "regresa"), ("g", "ne", "asigna"),
					# ("g", "ne", "lproc"), ("g", "ne", "imprime"), ("g", "ne", "imprimenl"), ("g", "ne", "leer"),
					# "interrumpe", "continua")],
Block 			= [("cg", "ne", ("g", "e", "estatuto"), ";",("g", "e", "Block"))]
BckEsp 			= [("|", "ne", ("g", "e", "estatuto"), ("cg", "ne", "inicio", ("g", "e", "Block"), "fin"))]
termino 		= [("|", "ne", ("cg", "ne", "(", ("g", "ne", "Exprlog"), ")"), ("t", "ne", keysList[7]), 
	      			("t", "ne", keysList[8]),("t", "ne", keysList[9]), ("t", "ne", keysList[10]))]										# Pending Id[lfunc|<Udim>] 
signo 			= ["[-", ("g", "ne", "termino")]
Expo 			= [("g", "ne", "signo"), ("cg", "e", "^", ("g", "ne", "Expo"))]
Multi 			= [("g", "ne", "Expo"), ("cg", "e", ("|", "ne", "*", "/", "%"), ("g", "ne", "Multi"))]
Expr 			= [("g", "ne", "Multi"), ("cg", "e", ("|", "ne", "+", "-"), ("g", "ne", "Expr"))]
Oprel 			= [("g", "ne", "Expr"), ("cg", "e", ("t", "ne", keysList[2]), ("g", "ne", "Opy"))]
Opno 			= [("cg", "ne", "[no", ("g", "ne", "Oprel"))],
Opy 			= [("g", "ne", "Opno"), ("cg", "e", "y", ("g", "ne", "Opy"))]
Exprlog 		= [("g", "ne", "Opy"), ("cg", "e", "o", ("g", "ne", "Exprlog"))]
si 				= ["si", "(", ("g", "ne", "Exprlog"), ")", "hacer", ("g", "e", "BckEsp"),
	  				("cg", "e", "sino", ("g", "e", "BckEsp"))]

grams = {
	"estatuto": 	estatuto,
	"Block": 		Block,
	"BckEsp": 		BckEsp,
	"termino": 		termino,
	"signo": 		signo,
	"Expo": 		Expo,
	"Multi": 		Multi,
	"Expr": 		Expr,
	"Oprel": 		Oprel,
	"Opno": 		Opno,
	"Opy":			Opy,
	"Exprlog":  	Exprlog,
	"si":       	si
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