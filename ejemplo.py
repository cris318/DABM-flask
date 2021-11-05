from flask import Flask,render_template,request,redirect
from flask.globals import request
import os
import random

from flask.helpers import locked_cached_property

app = Flask(__name__)

@app.route('/')
def inicio():
    return render_template('login.html')

@app.route('/datos')
def datos():
    user= {'nombre' : 'Cristian'}
    return render_template('datos.html',title='Titulo Personalizado',user=user)

@app.route('/menu',methods=["POST"])
def validar():
    if request.method=="POST":
        usuario=request.form['usuario']
        password=request.form['password']
        resultado=True
        resultado=verificar(usuario,password)
        if resultado ==True:
            return render_template('menu.html',title='Sistema DABM')
        else:
            resultado=False
            return redirect("/")
   

@app.route('/monitor')
def monitor():
    #consultar archivo de parametros
    datos=getDatos()
    # obtener lectura
    lectura=random.randint(0,45)
    # enviar a la interfaz
    color=0
    if lectura >= int(datos[0][1]) and lectura <= int(datos[0][2]):
        color=1 
    if lectura >= int(datos[1][1]) and lectura <= int(datos[1][2]):
        color=2 
    if lectura>= int(datos[2][1]) and lectura <= int(datos[2][2]):
        color=3

    return render_template("/monitor.html",datos=datos,lectura=lectura,color=color)
        
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

    for d in datos:
        if ((d[0]==usuario) and (d[1]==password)):
            return True

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
        
@app.route("/config")
def config():
    return render_template("config.html")


if __name__=="__main__":
    app.run(debug=True)