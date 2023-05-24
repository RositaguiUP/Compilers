from functions.variables import *
from functions.errors import *


def checkGrammar(lexemas):
    errors = []
    actualState = None

    lex = lexemas[0]
    actualState = State("Prgrm")
    gramToComp = grams[actualState.gram][actualState.index]
    res = checkLex(lex, 0, actualState, lexemas, gramToComp, True, errors)
    return res[0], res[4]

# checkLex returns: Error code, message, empty, i
# Error code:
#   0  = pass   
#   -2 = empty
#   -1 = error

def checkLex(lex, i, actualState, lexemas, gramToComp, parentEmpty, errors):
    errorMsg = ""
    empt = checkEmpty(gramToComp)                       # Could be empty

    if isinstance(gramToComp, str):                     # If it is a string
        if empt and len(gramToComp) > 1:
            gramToComp = gramToComp[1:]

        if lex[0] == gramToComp:                        # Are the same word
            parentEmpty =  False                        # If enters, it has to be completed even the cg/g could be empty
            return 0, errorMsg, parentEmpty, i, errors
        elif empt:
            return -2, errorMsg, parentEmpty, i, errors
        else:
            errorMsg = stringError(gramToComp, lex[2])          # Marks the error
            return -1, errorMsg, parentEmpty, i, errors

    elif isinstance(gramToComp, tuple):

        if (gramToComp[0] == "t"):                      # If it is a token
            if lex[1] == gramToComp[2]:                 # Have same token
                parentEmpty =  False                    # If enters, it has to be completed although the cg/g could be empty
                return 0, errorMsg, parentEmpty, i, errors
            elif empt:
                return -2, errorMsg, parentEmpty, i, errors
            else:
                errorMsg = tokenError(gramToComp[2], lex[2])          # Marks the error
                return -1, errorMsg, parentEmpty, i, errors
            
        elif (gramToComp[0] == "|"):                    # If it is an or -> one or another
            initialLex = lex
            for m in range(2, len(gramToComp)):         # Compare to all its possbile grammars
                gramToCompAux = gramToComp[m]
                if i >= len(lexemas):
                    line = lexemas[-1][2]
                    res = checkIfNextEmpty(i, gramToCompAux, errors, line)
                    return res
                lex = lexemas[i]
                res = checkLex(lex, i, actualState, lexemas, gramToCompAux, True, errors)
                
                if res[0] == 0:                         # Once one is fine, finish successfuly
                    i = res[3]
                    parentEmpty = res[2]                # if true, the parent grammar couldn't be empty
                    return 0, errorMsg, parentEmpty, i, errors
                elif res[0] == -1 and res[2] == False:
                    i = res[3]
                    parentEmpty = res[2]
                    return -1, errorMsg, res[2], i, errors
            if empt:
                errorMsg=[f"Expecting any '{actualState.gram}'", initialLex[2]]
                return -2, errorMsg, parentEmpty, i, errors
            else:
                return -1, errorMsg, parentEmpty, i, errors
        
        elif (gramToComp[0] == "g"):                    # If it is a grammar
            actualParent = parentEmpty
            actualState = State(gramToComp[2])
            parentErrorCode = 0
            while(True):                                # Compare to each element
                gramToCompAux = grams[actualState.gram][actualState.index]
                
                if i >= len(lexemas):
                    line = lexemas[-1][2]
                    res = checkIfNextEmpty(i, gramToCompAux, errors, line)
                    return res
                lex = lexemas[i]
                
                childEmpty = actualParent
                if checkEmpty(gramToCompAux):
                    childEmpty = True 

                res = checkLex(lex, i, actualState, lexemas, gramToCompAux, childEmpty, errors)
                
                gramLen = len(grams[actualState.gram])
                if res[0] == -1:
                    if empt and actualParent:
                        if res[2] == False:
                            i = res[3]
                            return -1, errorMsg, res[2], i, errors
                        else:
                            return -2, errorMsg, parentEmpty, i, errors
                    else:
                        if not childEmpty or res[2] == False:
                            parentErrorCode = -1
                            i = res[3]
                            actualParent = res[2]
                        else:
                            i = res[3]
                            return -1, errorMsg, res[2], i, errors
                else:
                    if res[0] == 0:
                        i = res[3] + 1
                        actualParent = res[2]           # if true, the parent grammar couldn't be empty

                actualState.addIndex()
                if actualState.index == gramLen:        # Finish when ends checking all the grammar elements
                    if parentErrorCode == 0:
                        i -= 1
                    return parentErrorCode, errorMsg, actualParent, i, errors
                
        elif (gramToComp[0] == "cg"):                   # If it is a compouned grammar
            actualParent = parentEmpty
            parentErrorCode = 0
            for k in range(2, len(gramToComp)):         # Compare to each of tis subgrammars
                gramToCompAux =  gramToComp[k]
                
                if i >= len(lexemas):
                    line = lexemas[-1][2]
                    res = checkIfNextEmpty(i, gramToCompAux, errors, line)
                    return res
                lex = lexemas[i]
                
                childEmpty = actualParent
                if checkEmpty(gramToCompAux):
                    childEmpty = True 
                
                res = checkLex(lex, i, actualState, lexemas, gramToCompAux, childEmpty, errors)
                
                if res[0] == -1:
                    if empt and actualParent:
                        if res[2] == False:
                            i = res[3]
                            return -1, errorMsg, res[2], i, errors
                        else:
                            return -2, errorMsg, parentEmpty, i, errors
                    else:
                        if not childEmpty or res[2] == False:
                            errorMsg = res[1]
                            if errorMsg != "":
                                errors.append(errorMsg)
                            errorMsg = ""
                            parentErrorCode = -1
                            i = res[3]
                            actualParent = res[2]
                        else:
                            i = res[3]
                            return -1, errorMsg, res[2], i, errors
                elif res[0] == 0:
                    i = res[3] + 1
                    actualParent = res[2]               # if true, the parent grammar couldn't be empty
            if parentErrorCode == 0:
                i -= 1
            return parentErrorCode, errorMsg, actualParent, i, errors

        
                        # if parentErrorCode != 0:
                        #     return parentErrorCode, errorMsg, parentEmpty, i
                        # else:
    
def checkIfNextEmpty(i, gramToComp, errors, line):
    errorMsg = ""
    empt = checkEmpty(gramToComp)
    if empt:
        return 0, errorMsg, False, i, errors
    else:
        if isinstance(gramToComp, str):     # If is a string
            if empt == True:
                gramToComp = gramToComp[1:]
            errorMsg += stringError(gramToComp, line)
        elif isinstance(gramToComp, tuple):
            if (gramToComp[0] == "t"): 
                errorMsg += tokenError(gramToComp, line)
        errors.append(errorMsg)
        return -1, errorMsg, False, i, errors
    
def checkEmpty(gramToComp):
    empt = False
    if isinstance(gramToComp, str):     # If is a string
        if gramToComp.startswith('[') and len(gramToComp) > 1:
            empt = True
    elif isinstance(gramToComp, tuple):
        if gramToComp[1] == "e":
            empt = True
    return empt
    
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
