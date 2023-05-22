from variables import *



def checkGrammar(lexemas):
    openState = False
    id = 0
    states = []
    parentState = None
    actualState = None
    i = 0
    while i < len(lexemas):
        lex = lexemas[i]
        if (openState == False):
            for gramKey in gramsKeysList:
                if lex[0] == grams[gramKey][0]:
                    parentState = State(gramKey, 0, id)
                    actualState = parentState
                    states.append(parentState)
                    openState = True
                    id += 1
                    break
        else:
            parentState.addIndex()
            gramToComp = grams[actualState.gram][actualState.index]
            res = checkLex(lex, i, parentState, parentState, lexemas, gramToComp)
            if res == -1:
                parentState.index -= 1
                return -1
            else:
                i = res
        i += 1
    return 1

def checkLex(lex, i, actualState, parentState, lexemas, gramToComp):
    if isinstance(gramToComp, str):     # If is a string
        empt = False
        if gramToComp.startswith('[') and len(gramToComp) > 1:
            empt = True
            gramToComp = gramToComp[1:]

        if lex[0] == gramToComp:
            return i
        elif empt == True:
            return 0
        else:
            return -1
    elif isinstance(gramToComp, tuple):
        empt = False                             # Could be empty
        if gramToComp[1] == "e":
            empt = True

        if (gramToComp[0] == "cg"):              # If is a compuned grammar
            for k in range(2, len(gramToComp)):
                if i >= len(lexemas):
                    return -1
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, actualState, lexemas, gramToComp[k])
                if res == -1:
                    if empt == False:
                        return -1
                    else:
                        return 0
                elif res != 0:
                    i = res + 1
            i -= 1
            return i
        
        elif (gramToComp[0] == "g"):            # If is a grammar
            actualState = State(gramToComp[2], parentState.parentId, parentState.index+1)
            parentState.substates.append(actualState)
            parentState.substateStart = True
            while(True):
                if i >= len(lexemas):
                    return -1
                lex = lexemas[i]
                gramToCompAux = grams[actualState.gram][actualState.index]
                res = checkLex(lex, i, actualState, actualState, lexemas, gramToCompAux)
                if res == -1:
                    if empt == False:
                        return -1
                    else:
                        return 0
                else:
                    gramLen = len(grams[actualState.gram])
                    actualState.addIndex()
                    if res != 0:
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
                return 0
            
        elif (gramToComp[0] == "|"):
            for m in range(2, len(gramToComp)):
                if i >= len(lexemas):
                    return -1
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, actualState, lexemas, gramToComp[m])
                if res > 0:
                    return i
            if (empt == False):
                return -1
            else:
                return 0
            
    elif isinstance(gramToComp, list):
        for l in range(len(gramToComp)):
            if i >= len(lexemas):
                return -1
            lex = lexemas[i]
            res = checkLex(lex, i, actualState, actualState, lexemas, gramToComp[l])
            if  res == -1:
                return -1
            elif res != 0:
                i = res + 1
        i -= 1
        return i