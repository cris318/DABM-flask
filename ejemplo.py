from flask import Flask,render_template,request
from flask.globals import request
import os
import random

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/datos')
def datos():
    user= {'nombre' : 'Cristian'}
    return render_template('datos.html',title='Titulo Personalizado',user=user)

@app.route('/validar',methods=["POST"])
def validar():
    if request.method=="POST":
        usuario=request.form['usuario']
        password=request.form['password']

        resultado=verificar(usuario,password)
        if resultado ==True:
            return render_template('menu.html',title='Sistema DABM')
        else:
            return render_template('login.html')
        #return usuario +";"+ password

@app.route('/monitor')
def monitor():
    #consultar archivo de parametros
    datos=getDatos()
    #print(datos)
    # obtener lectura
    lectura=random.randint(0,45)
    # enviar a la interfaz
    return render_template("/monitor.html",datos=datos,lectura=lectura)
        
def verificar(usuario,password):
    directorio=os.path.dirname(__file__)        #se abre y lee el archivo de texto de "users.cvs"
    nombrearchivo="bd/users.csv"
    ruta=os.path.join(directorio,nombrearchivo)

    f= open(ruta,"r")
    lineas=f.readlines()        #leemos las lineas del archivo de texto
    f.close()
    datos=[]                    #lista donde vamos a almacenar cada fila del  archivo de texto
    for l in lineas:
        l=l.replace("\n","")
        l=l.split(";")
        datos.append(l)
        #print(l)
    for d in datos:
        if ((d[0]==usuario) & (d[1]==password)):
            return True
        #usuario no exite,contraseña correcta,bienvenido
   




def getDatos():
    directorio=os.path.dirname(__file__)
    nombrearchivo="bd/parametros.csv"
    ruta=os.path.join(directorio,nombrearchivo)

    f= open(ruta,"r")
    lineas=f.readlines()
    f.close()
    datos=[]
    for l in lineas:
        l=l.replace("\n","")
        l=l.split(";")
        datos.append(l)
    return datos
if __name__=="__main__":
    app.run(debug=True)