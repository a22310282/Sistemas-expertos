PERSONAJES = [
    {'id':1,'nombre':'Ana','genero':'femenino','pelo':'rubio','gafas':False,'sombrero':False,'barba':False},
    {'id':2,'nombre':'Carlos','genero':'masculino','pelo':'negro','gafas':True,'sombrero':False,'barba':True},
    {'id':3,'nombre':'Luisa','genero':'femenino','pelo':'castaño','gafas':True,'sombrero':False,'barba':False},
    {'id':4,'nombre':'Pedro','genero':'masculino','pelo':'rubio','gafas':False,'sombrero':True,'barba':True},
    {'id':5,'nombre':'María','genero':'femenino','pelo':'negro','gafas':False,'sombrero':True,'barba':False},
]

ATRIBUTOS = ['genero','pelo','gafas','sombrero','barba']

def personaje_by_id(pid: int):
    return next(x for x in PERSONAJES if x['id']==pid)
