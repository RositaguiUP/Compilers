
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
				"imprimeln", "verdadero", "falso"]),                           #4
	"<OpAsig>":  set([":="]),    #5
	"<Ident>":   set(),          #6
	"<CteEnt>":  set(),          #7
	"<CteReal>": set(),          #8
	"<CteAlfa>": set(),          #9
	"<CteLog>":  set(),          #10
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
# Block 			= ["[", "<estatuto>", "]", ";", "[", "<Block>", "]"],
# estatuto 		= ["<si>", "|", "limpiar", "|", "<desde>", "|", "<repetir>", "|", "<mientras>", "|", "<cuando>", "|", "<regresa>", "|", "<asigna>", "|", "<lproc>", "|", "<imprime>", "|", "<imprimenl>", "|", "<leer>", "|", "interrumpe", "|", "continua"],






# Exprlog 		= [Opy]
# ExprlogAux 		= ("cg", "e", "o", Exprlog)
# Exprlog.append(ExprlogAux)





# BckEsp 			= ["[", "<estatuto>", "]", "|", "inicio", "[", "<Block>", "]", "fin"],
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
# Multi 			= ["<Expo>", "[", "*", "|", "/", "|", "%", "<Multi>", "]"],
# Expo 			= ["<signo>", "[", "^", "<Expo>", "]"],
# signo 			= ["[-]", "<termino>"],
# termino 		= ["Id", "[", "lfunc", "|", "<Udim>", "]", "|", "(", "<Exprlog>", ")", "|", "CteEnt", "|", "CteReal", "|", "CteAlfa", "|", "verdadero", "|", "falso"],
# lproc 			= ["Id", "(", "<Uparams>", ")"],
# lfunc 			= ["Id", "(", "<Uparams>", ")"],
# imprime 		= ["imprime", "(", "<GpoExp>", ")"],
# imprimenl 		= ["imprimenl", "(", "<GpoExp>", ")"],
# GpoExp 			= ["<Exprlog>", "[", ",", "<GpoExp>", "]"],
# Uparams 		= ["<Explog>", "[", ",", "<Uparams>", "]"],
# impi 			= ["limpia"],
# leer 			= ["lee", "(", "Id", "[", "<Udim>", "]", ")"]

# Exprlog  = [("t", "ne", keysList[7]), ("t", "ne", keysList[2]), ("t", "ne", keysList[7])]
# si       = ["si", "(", ("g", "ne", "Exprlog"), ")", "hacer"]

Expr 			= [("t", "ne", keysList[7])] #["<Multi>", "[", "+", "|", "-", "<Expr>", "]"]
Oprel 			= [("g", "ne", "Expr"), ("cg", "e", ("t", "ne", keysList[2]), ("g", "ne", "Opy"))]
Opno 			= [("cg", "ne", "[no", ("g", "ne", "Oprel"))],
Opy 			= [("g", "ne", "Opno"), ("cg", "e", "y", ("g", "ne", "Opy"))]
Exprlog 		= [("g", "ne", "Opy"), ("cg", "e", "o", ("g", "ne", "Exprlog"))]
si 				= ["si", "(", ("g", "ne", "Exprlog"), ")", "hacer"] #, "[", "<BckEsp>", "]", "[", "sino", "[", "<BckEsp>", "]", "]"],



grams = {
	"Expr": 	Expr,
	"Oprel": 	Oprel,
	"Opno": 	Opno,
	"Opy":		Opy,
	"Exprlog":  Exprlog,
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