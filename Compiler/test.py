

def testa(a):
    if a == 0:
        return 0, ""
    else:
        return -1, "mal"
    

res = testa(0)

print("res: ", res)
if res == -1:
    print("msg: ", msg)