"""
Conjunto de vertices ordenados horizontal en arbol
"""
def BusquedaHorizontal(Raiz,Grafo):
    V=list(Grafo.keys())
    S=[Raiz]
    Vp=[Raiz]
    Ep=[]
    Vd=V.copy()
    Vd.remove(Raiz)
    Vtemporal=Vd.copy()
    s=[]
    
    while True:
        for x in S:
            for y in Vtemporal:
                    if y in Grafo[x]:
                        Vp.append(y)
                        Ep.append((x,y))
                        s.append(y)
                        Vd.remove(y)
            Vtemporal=Vd.copy()
        if s==[]:        
            T=(Vp,Ep)
            return T
            break
        S=s.copy()
        s=[]
        

G = {"a":["b","c","g"],"b":["a","d"],"c":["a","e","d"],"g":["a","e"],"d":["b","f","c"],"e":["f","g","c"],"f":["e","h","d"],"h":["f"]}
R = "a"


print(BusquedaHorizontal(R,G))
            
                    

                    
