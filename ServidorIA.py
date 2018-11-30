

import face_recognition
import numpy as np
import cv2
from os import listdir
from os.path import isfile, join   

import os.path
import os

import datetime

from flask import Flask, jsonify, request, redirect

dateTimeActual = datetime.datetime.now()


# You can change this to any folder on your system
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/index', methods=['GET', 'POST'])
def index():
	# Check if a valid image file was uploaded
    if request.method == 'POST':
        MostrarLogConsola("Recibiendo POST prueba local")
        if 'file' not in request.files:
            MostrarLogConsola("no hay un file en la solicitud")
            return redirect(request.url)
        else:
            file = request.files['file']

            if file.filename == '':
                MostrarLogConsola("solicitud vacia")
                return redirect(request.url)

            if file and allowed_file(file.filename):
                MostrarLogConsola("El archivo es correcto... procesando imagen")
                nombre, respuesta = detect_faces_in_image(file)
                personaReconocida = "Persona reconocida: %s" %(nombre)
                ipCliente = request.environ['REMOTE_ADDR']
                LlenarLogAuditoria(ipCliente, personaReconocida)
                return respuesta
    else:
        MostrarLogConsola("Error no se recibio POST")
    
    return '''
    <!doctype html>
    <title>Servidor IA</title>
    <h1>Servidor de Reconocimiento Facial FCV</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''


@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
	# Check if a valid image file was uploaded
    if request.method == 'POST':
        MostrarLogConsola("Recibiendo POST para registrar.")
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # The image file seems valid! Detect faces and return the result.
            nombreFoto = request.form['nameFile']
            resultado = guardarImagen(file,nombreFoto)
            ActualizarBaseDatos()      
            personaRegistrada = "Registrando a %s y actualizada la base de datos." %(nombreFoto)
            ipCliente = request.environ['REMOTE_ADDR']
            LlenarLogAuditoria(ipCliente, personaRegistrada)
            return resultado
			

    else:
        MostrarLogConsola("Error no se recibio POST")


    
    return '''
    <!doctype html>
	<h1>Servidor de Reconocimiento Facial FCV</h1>
    '''


@app.route('/', methods=['GET', 'POST'])
def upload_image():
    # Check if a valid image file was uploaded
    if request.method == 'POST':
        if 'file' not in request.files:
            MostrarLogConsola("no hay un file en la solicitud")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            MostrarLogConsola("solicitud vacia")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            MostrarLogConsola("El archivo es correcto... procesando imagen")
            nombre, respuesta = detect_faces_in_image(file)
            personaReconocida = "Persona reconocida: %s" %(nombre)
            ipCliente = request.environ['REMOTE_ADDR']
            LlenarLogAuditoria(ipCliente, personaReconocida)
            return respuesta

    # If no valid image file was uploaded, show the file upload form:
    return '''
    <!doctype html>
	<h1>Servidor de Reconocimiento Facial FCV</h1>
    '''
	

	
ArchivoCodificadoDatos = "pictures_encoded/data.csv"
ArchivoCodificadoNombres = "pictures_encoded/names.csv"

def MostrarLogConsola(datos):
    infoGuardar = 'echo "%s" >> /var/log/ia.log ' %(datos)
    os.system(infoGuardar)
    print(datos)

def LlenarLogAuditoria(ipCliente, tipoSolicitud):
    datosFechaHoraActual = dateTimeActual
    datosGuardar = "%s - %s - %s \n" %(datosFechaHoraActual, ipCliente, tipoSolicitud)
    f=open("logAuditoria.bin",'a')
    f.write(datosGuardar)
    f.close()
    MostrarLogConsola(datosGuardar)
   	
def LeerArchivoTexto(urlArchivo):
    f = open (urlArchivo,'r')
    mensaje = f.read()
    return mensaje

def leerArrayNombres(): 
    datosProcesar = LeerArchivoTexto(ArchivoCodificadoNombres)
    datosProcesar = datosProcesar[1:-1]
    ArrayNombres = datosProcesar.split(',')
    return ArrayNombres	
	
def leerArrayDatos():
    datoString = LeerArchivoTexto(ArchivoCodificadoDatos)
    matrixDatosRostros = []
    b = datoString.replace("[[","").replace("\n","")
    numeroPaquetes = b.count("],")
    #MostrarLogConsola("numero Rostros en la Base de Datos Codificada: %d" %(numeroPaquetes))

    for paquete in b.split('],'):
        paquete = paquete.replace("[","")
        #cantidadDatosPaquete = paquete.count(",")
        #MostrarLogConsola("cantidad Datos Paquete: %d" %(cantidadDatosPaquete))
        
        if len(paquete)>10:   
            ListaDatosString = paquete.split(',')
            listaDatosFloat = [ float(i) for i in  ListaDatosString]  #convierto cada item de la cadena a float
            ArrayDatos = np.array(listaDatosFloat)
            matrixDatosRostros.append(ArrayDatos)   
    return matrixDatosRostros	
	
def guardarImagen(file_stream, nameFile):	
    img = face_recognition.load_image_file(file_stream)	
    nombreImagen = "pictures_of_people_i_know/" + nameFile + ".jpeg"   	
    status = cv2.imwrite(nombreImagen,img)
	
    result = {
        "nameFile": nombreImagen,
        "estadoGuardadoImagen": status
    }
    return jsonify(result)
	
def detect_faces_in_image(file_stream):
    img = face_recognition.load_image_file(file_stream)
    ubicacionRostro = face_recognition.face_locations(img)
    unknown_face_encodings = face_recognition.face_encodings(img, ubicacionRostro)

    face_found = False
    face_fecognition = False
    nombre = "Sin Identificar"
	
    datos = leerArrayDatos()

    if len(datos) > 0:
        face_found = True
		
        if np.ndim(unknown_face_encodings) > 1:
            match_results = face_recognition.compare_faces(datos, unknown_face_encodings[0], 0.50)
            if True in match_results:
                face_fecognition = True
                indice = match_results.index(True)
                nombre = leerArrayNombres()[indice]
                            #una vez identificada la imagen de la persona en la base de datos existente, se debe reemplazar la imagen original por la imagen "file_stream"
                            #borrar la anterior imagen y guardar la nueva imagen con el mismo nombre
		

    result = {
        "rostroEncontrado": face_found,
        "personaConocida": face_fecognition,
        "nombrePersona": nombre
    }
    return nombre, jsonify(result)
	
def cargarImagen(urlImagen):
    img = face_recognition.load_image_file(urlImagen)
    return img	
	
def codificarArchivo(urlImagen):
    img = cargarImagen(urlImagen)
    face_encoding1 = face_recognition.face_encodings (img) [ 0 ]
    return face_encoding1	
	
def listaDatos_Nombres():
    ListaConocidos = []
    ruta = "pictures_of_people_i_know"
    ListaConocidos = [arch for arch in listdir(ruta) if isfile(join(ruta, arch))]
    ListaArchivos = []
    ListaNombres = []
    for item in ListaConocidos:
        ListaArchivos.append(item)
        ListaNombres.append(item.replace(".jpeg",""))
    ListaArrayDatos = []
    for archivo in ListaArchivos:
        face_encoding = codificarArchivo("pictures_of_people_i_know/" + archivo)
        ListaArrayDatos.append(face_encoding)
    return ListaArrayDatos, ListaNombres	
	
def ajustarStringInfo(Info):
    datosGuardar = "[" + Info + "]"
    return datosGuardar	
	
def GuardarArchivosCodificados(ArrayDatos, ArrayNombres):
    f = open(ArchivoCodificadoDatos, "w")
    
    datosGuardar = ""
    for ArrayPersona in ArrayDatos:
        s = np.array2string(ArrayPersona, separator=',', formatter={'float_kind':lambda x: "%.8f" % x})
        datosGuardar = datosGuardar + s + ","        
    datosGuardar = ajustarStringInfo (datosGuardar )
    f.write(datosGuardar)
    f.close()
    
    f = open(ArchivoCodificadoNombres, "w")
    s = ajustarStringInfo (','.join(ArrayNombres) )  
    f.write(s)
    f.close()	
	
def ActualizarBaseDatos():
    known_face_encodings,known_face_names = listaDatos_Nombres()
    GuardarArchivosCodificados(known_face_encodings, known_face_names)	

MostrarLogConsola("Servidor iniciado.")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
    
MostrarLogConsola("Servidor terminado.")
