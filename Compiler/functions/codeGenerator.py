def hashTable(lexemas, tablaSimbolos):
    declare = False
    names = []
    CVIPF = None
    Tipo = "E"
    D1 = 0
    D2 = 0
    Dimensiones = []
    for lexema in lexemas:
        if D1 == -1:
            D1 = lexema[0]

        elif D2 == -1:
            D2 = lexema[0]

        elif lexema[0] == 'constantes':
            CVIPF = 'C'
            declare = True
        elif lexema[0] == 'variables':
            CVIPF = 'V'
            declare = True
        #elif lexema[0] == 'procedimiento':
        #    CVIPF = 'P'
        #    declare = True
        #elif lexema[0] == 'funcion':
        #    CVIPF = 'F'
        #    declare = True

        elif lexema[0] == 'entero' or lexema[1] == '<CteEnt>':
            Tipo = "E"
        elif lexema[0] == 'real' or lexema[1] == '<CteReal>':
            Tipo = "R"
        elif lexema[0] == 'alfabetico' or lexema[1] == '<CteAlfa>':
            Tipo = "A"
        elif lexema[0] == 'logico' or lexema[1] == '<CteLog>':
            Tipo = "L"

        elif lexema[0] == ':' or lexema[0] == ',' or (CVIPF == 'C' and lexema[0] == ':=') and declare:
            Dimensiones.append((D1,D2))
            D1 = 0
            D2 = 0

        elif lexema[0] == '[' and declare:
            if D1 != 0:
                D2 = -1
            else:
                D1 = -1
            
        elif lexema[1] == '<Ident>' and declare:
            names.append(lexema[0])

        elif lexema[0] == ';' and declare:
            for i,name in enumerate(names):
                fila = []
                fila.append(CVIPF)
                fila.append(Tipo)
                fila.append(str(Dimensiones[i][0]))
                fila.append(str(Dimensiones[i][1]))
                fila.append("#")
                tablaSimbolos[name] = fila
            Dimensiones = []
            names = []

        elif lexema[1] == '<PalRes>':
            declare = False

    with open("Test_0.eje", "w+") as nf:
        for fila in tablaSimbolos:
            nf.write(fila + ",")
            for columna in tablaSimbolos[fila]:
                nf.write(columna + ",")
            nf.write("\n")


def codeGenerator(lexemas):
    for lexema in lexemas:
        if lexema[0] == 'constantes':
            pass
        if lexema[0] == 'variables':
            pass
