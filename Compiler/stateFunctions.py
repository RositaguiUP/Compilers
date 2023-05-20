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
            res = checkLex(lex, i, parentState, parentState, lexemas)
            if res == -1:
                parentState.index -= 1
                return -1
            else:
                i = res
        i += 1
    return 1

def checkLex(lex, i, actualState, parentState, lexemas):
    gramToComp = grams[actualState.gram][actualState.index]
    if isinstance(gramToComp, str):     # If is a string
        if lex[0] == grams[actualState.gram][actualState.index]:
            return i
        else:
            return -1
    elif isinstance(gramToComp, tuple):   # If is a grammar
        if (gramToComp[0] == "g"):
            actualState = State(gramToComp[1], parentState.parentId, parentState.index+1)
            parentState.substates.append(actualState)
            parentState.substateStart = True
            while(True):
                lex = lexemas[i]
                if checkLex(lex, i, actualState, actualState, lexemas) == -1:
                    return -1
                else:
                    gramLen = len(grams[actualState.gram])
                    actualState.addIndex()
                    i += 1
                    if actualState.index == gramLen:
                        actualState.index -= 1
                        i -= 1
                        return i

        else:                               # If is a token
            if lex[1] == gramToComp[1]:
                return i
            else:
                return -1
