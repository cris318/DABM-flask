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
        return render_template('menu.html',title='Sistema DABM')

        #return usuario +";"+ password

def verificar(usuario,password):
    #usuario no exite,contraseña correcta,bienvenido
    return True

if __name__=="__main__":
    app.run(debug=True)