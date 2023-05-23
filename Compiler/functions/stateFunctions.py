from functions.variables import *



def checkGrammar(lexemas):
    openState = False
    id = 0
    actualState = None

    lex = lexemas[0]
    actualState = State("Prgrm", 0, id)
    gramToComp = grams[actualState.gram][actualState.index]
    res = checkLex(lex, 0, actualState, actualState, lexemas, gramToComp)
    if res >= 0:
        return 1
    return -1

    # i = 0
    # while i < len(lexemas):
    #     lex = lexemas[i]
    #     if openState == False:
    #         for gramKey in gramsKeysList:
    #             actualState = State(gramKey, 0, id)
    #             while actualState.index < len(grams[actualState.gram]):
    #                 gramToComp = grams[actualState.gram][actualState.index]
    #                 res = checkLex(lex, i, actualState, actualState, lexemas, gramToComp)
    #                 actualState.addIndex()
    #                 if res == -1:
    #                     break
    #                 elif res >= 0:
    #                     openState = True
    #                     i = res + 1
    #                     break
    #             if openState == True:
    #                 break
    #         if openState == False:
    #             return -1
    #     openState = False
    # return 1

def checkLex(lex, i, actualState, parentState, lexemas, gramToComp):
    if isinstance(gramToComp, str):     # If is a string
        empt = False
        if gramToComp.startswith('[') and len(gramToComp) > 1:
            empt = True
            gramToComp = gramToComp[1:]

        if lex[0] == gramToComp:
            return i
        elif empt == True:
            return -2
        else:
            return -1
    elif isinstance(gramToComp, tuple):
        empt = False                             # Could be empty
        if gramToComp[1] == "e":
            empt = True

        if (gramToComp[0] == "cg"):              # If is a compuned grammar
            for k in range(2, len(gramToComp)):
                gramToCompAux =  gramToComp[k]
                if i >= len(lexemas):
                    return checkEmpty(i, gramToCompAux)
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, actualState, lexemas, gramToCompAux)
                if res == -1:
                    if empt == False:
                        return -1
                    else:
                        return -2
                elif res >= 0:
                    i = res + 1
            i -= 1
            return i
        
        elif (gramToComp[0] == "g"):            # If is a grammar
            actualState = State(gramToComp[2], parentState.parentId, parentState.index+1)
            parentState.substates.append(actualState)
            parentState.substateStart = True
            while(True):
                gramToCompAux = grams[actualState.gram][actualState.index]
                if i >= len(lexemas):
                    return checkEmpty(i, gramToCompAux)
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, actualState, lexemas, gramToCompAux)
                if res == -1:
                    if empt == False:
                        return -1
                    else:
                        return -2
                else:
                    gramLen = len(grams[actualState.gram])
                    actualState.addIndex()
                    if res != -2:
                        i = res + 1
                if actualState.index == gramLen:
                    actualState.index -= 1
                    i -= 1
                    return i

        elif (gramToComp[0] == "t"):           # If is a token
            if lex[1] == gramToComp[2]:
                return i
            elif (empt == False):
                return -1
            else:
                return -2
            
        elif (gramToComp[0] == "|"):
            for m in range(2, len(gramToComp)):
                gramToCompAux = gramToComp[m]
                if i >= len(lexemas):
                    return checkEmpty(i, gramToCompAux)
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, actualState, lexemas, gramToCompAux)
                if res >= 0:
                    i = res
                    return i
            if (empt == False):
                return -1
            else:
                return -2
    
def checkEmpty(i, gramToComp):
    empt = False
    if isinstance(gramToComp, str):     # If is a string
        if gramToComp.startswith('[') and len(gramToComp) > 1:
            empt = True
    elif isinstance(gramToComp, tuple):
        if gramToComp[1] == "e":
            empt = True
    if empt:
        return i
    else:
        return -1

def hashTable(lexemas):
    declare = False
    names = []
    CVIP = None
    Tipo = "E"
    D1 = 0
    D2 = 0
    tablaSimbolos = []
    for lexema in lexemas:
        if lexema[0] == 'constantes':
            CVIP = 'C'
            declare = True
        elif lexema[0] == 'variables':
            CVIP = 'V'
            declare = True

        elif lexema[0] == 'entero' or lexema[1] == '<CteEnt>':
            Tipo = "E"
        elif lexema[0] == 'real' or lexema[1] == '<CteReal>':
            Tipo = "R"
        elif lexema[0] == 'alfabetico' or lexema[1] == '<CteAlfa>':
            Tipo = "A"

        elif lexema[1] == '<Ident>':
            names.append(lexema[0])
        
        elif lexema[0] == ';' and declare:
            for name in names:
                fila = []
                fila.append(name)
                fila.append(CVIP)
                fila.append(Tipo)
                fila.append(str(D1))
                fila.append(str(D2))
                fila.append("#")
                tablaSimbolos.append(fila)
            names = []

        elif lexema[1] == '<PalRes>':
            declare = False

    with open("Test_0.eje", "w+") as nf:
        for fila in tablaSimbolos:
            for columna in fila:
                nf.write(columna + ",")
            nf.write("\n")
            


def codeGenerator(lexemas):
    for lexema in lexemas:
        if lexema[0] == 'constantes':
            pass
        if lexema[0] == 'variables':
            pass
