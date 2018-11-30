import face_recognition
import numpy as np

from os import listdir
from os.path import isfile, join    

import os.path
import os



temporalDatos = "temporal/nuevoDatos.csv"
temporalNombres = "temporal/nuevoNombres.csv"
temporalCopiando = "temporal/copiando.txt"
existeTemporales = "temporal/hayTemporales.txt"

ArchivoCodificadoDatos = "pictures_encoded/data.csv"
ArchivoCodificadoNombres = "pictures_encoded/names.csv"

def ExisteArchivo(url):
    return os.path.isfile(url)

def ajustarStringInfo(Info):
    datosGuardar = "[" + Info + "]"
    return datosGuardar

def borrarArchivo(url):
    os.remove(url)	
	
def crearArchivo(url):
    file = open(url,"w")
    file.write("Wisrovi.rodriguez@gmail.com")
    file.close()

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

def ActualizarBaseDatosTemporales():
    print("Creando Archivos temporales")
    ArrayDatos,ArrayNombres = listaDatos_Nombres()    
    crearArchivo(temporalCopiando)
    
    f = open(temporalDatos, "w")
    datosGuardar = ""
    for ArrayPersona in ArrayDatos:
        s = np.array2string(ArrayPersona, separator=',', formatter={'float_kind':lambda x: "%.8f" % x})
        datosGuardar = datosGuardar + s + ","        
    datosGuardar = ajustarStringInfo (datosGuardar )
    f.write(datosGuardar)
    f.close()
    print("Archivos temporal de datos creado")
    
    f = open(temporalNombres, "w")
    s = ajustarStringInfo (','.join(ArrayNombres) )  
    f.write(s)
    f.close()
    print("Archivos temporal de nombres creado")
    
    borrarArchivo(temporalCopiando)
    if ExisteArchivo(temporalCopiando)==True:
        borrarArchivo(temporalCopiando)
    
    crearArchivo(existeTemporales)
    if ExisteArchivo(existeTemporales)==False:
        crearArchivo(existeTemporales)
    print("Finalizando creacion archivos temporales")

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
    
	
	
	
ActualizarBaseDatos()	
	
ActualizarBaseDatosTemporales()