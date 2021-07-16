
from Query import Busqueda
from flask import Flask, render_template, request
import socket
app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def home():
   
    if request.method == 'POST':
        if request.form['submit_button'] == 'update':
          palabra=request.form['palabra']
          opcion=request.form['opcion'] 
          aux=Busqueda(palabra,opcion)  
          ##descarga ontologia
          #aux.download()   
          s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
          s.settimeout(5)
          try:
             s.connect(("www.google.com", 80))
          except (socket.gaierror, socket.timeout):
             print("Sin conexión a internet")
             resultado=aux.consulta()
          else:
             resultado=aux.consultaConectado()
             s.close()                     
        return render_template('index.html',contenido=resultado[0],texto=palabra, imagen=resultado[1])
    else:
        return render_template('index.html',contenido="",texto="",imagen="https://icon-library.com/images/default-profile-icon/default-profile-icon-17.jpg")
if __name__ == '__main__':
    app.run(debug=True)
