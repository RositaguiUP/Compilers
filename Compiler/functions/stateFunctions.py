from functions.variables import *
from functions.errors import *


def checkGrammar(lexemas):
    errors = []
    actualState = None

    lex = lexemas[0]
    actualState = State("Prgrm")
    gramToComp = grams[actualState.gram][actualState.index]
    res = checkLex(lex, 0, actualState, lexemas, gramToComp, True)
    if res[0] >= 0:
        return 1
    return -1

# checkLex returns:
#   i  = pass
#   -2 = empty
#   -1 = error

def checkLex(lex, i, actualState, lexemas, gramToComp, parentEmpty):
    errorMsg = ""

    if isinstance(gramToComp, str):                 # If it is a string
        empt = False
        if gramToComp.startswith('[') and len(gramToComp) > 1:
            empt = True
            gramToComp = gramToComp[1:]

        if lex[0] == gramToComp:                    # Are the same word
            return i, errorMsg, parentEmpty
        elif empt:
            return -2, errorMsg, parentEmpty
        else:
            errorMsg = stringError(gramToComp)
            return -1, errorMsg, parentEmpty

    elif isinstance(gramToComp, tuple):
        empt = False                                
        if gramToComp[1] == "e":                    # Could be empty
            empt = True

        elif (gramToComp[0] == "t"):                # If it is a token
            if lex[1] == gramToComp[2]:             # Have same token
                if i > 0:
                    parentEmpty =  False
                return i, errorMsg, parentEmpty
            elif empt:
                return -2, errorMsg, parentEmpty
            else:
                return -1, errorMsg, parentEmpty
            
        elif (gramToComp[0] == "|"):                # If it is an or -> one or another
            for m in range(2, len(gramToComp)):     # Compare to all its possbile grammars
                gramToCompAux = gramToComp[m]
                if i >= len(lexemas):
                    return checkEmpty(i, gramToCompAux)
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, lexemas, gramToCompAux, parentEmpty)
                if res[0] >= 0:                     # Once one is fine, finish successfuly
                    i = res[0]
                    parentEmpty = res[2]
                    return i, errorMsg, parentEmpty
            if empt:
                return -2, errorMsg, parentEmpty
            else:
                return -1, errorMsg, parentEmpty

        if (gramToComp[0] == "cg"):                 # If it is a compuned grammar
            for k in range(2, len(gramToComp)):     # Compare to each of tis subgrammars
                gramToCompAux =  gramToComp[k]
                if i >= len(lexemas):
                    return checkEmpty(i, gramToCompAux)
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, lexemas, gramToCompAux, parentEmpty)
                if res[0] == -1:
                    if empt:
                        return -2, errorMsg, parentEmpty
                    else:
                        if (i != 0 and not parentEmpty):
                            errorMsg = res[1]
                            print(errorMsg)
                        return -1, errorMsg, parentEmpty
                elif res[0] >= 0:
                    i = res[0] + 1
                    parentEmpty = res[2]
            i -= 1
            return i, errorMsg, parentEmpty
        
        elif (gramToComp[0] == "g"):                # If it is a grammar
            actualState = State(gramToComp[2])
            while(True):                            # Compare to each element
                gramToCompAux = grams[actualState.gram][actualState.index]
                if i >= len(lexemas):
                    return checkEmpty(i, gramToCompAux)
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, lexemas, gramToCompAux, parentEmpty)
                if res[0] == -1:
                    if empt:
                        return -2, errorMsg, parentEmpty
                    else:
                        return -1, errorMsg, parentEmpty
                else:
                    gramLen = len(grams[actualState.gram])
                    actualState.addIndex()
                    if res[0] != -2:
                        i = res[0] + 1
                        parentEmpty = res[2]
                if actualState.index == gramLen:    # Finish when ends checking all the grammar elements
                    actualState.index -= 1
                    i -= 1
                    return i, errorMsg, parentEmpty

        
    
def checkEmpty(i, gramToComp):
    errorMsg = ""
    empt = False
    if isinstance(gramToComp, str):     # If is a string
        if gramToComp.startswith('[') and len(gramToComp) > 1:
            empt = True
    elif isinstance(gramToComp, tuple):
        if gramToComp[1] == "e":
            empt = True
    if empt:
        return i, errorMsg, False
    else:
        return -1, errorMsg, False
    
    # openState = False
    # id = 0
    # i = 0
    # while i < len(lexemas):
    #     lex = lexemas[i]
    #     if openState == False:
    #         for gramKey in gramsKeysList:
    #             actualState = State(gramKey, 0, id)
    #             while actualState.index < len(grams[actualState.gram]):
    #                 gramToComp = grams[actualState.gram][actualState.index]
    #                 res = checkLex(lex, i, actualState, lexemas, gramToComp)
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


    # si el padre es empty -> el error no cuenta,
    #       a menos que encuentre un no empty que si