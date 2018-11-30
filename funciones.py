import face_recognition
import numpy as np
import time
from funcionesArchivos import *

ArchivoCodificadoDatos = "pictures_encoded/data.csv"
ArchivoCodificadoNombres = "pictures_encoded/names.csv"

def pausarSegundos(tiempo = 0.1):
    time.sleep(tiempo)

def cargarImagen(urlImagen):
    img = face_recognition.load_image_file(urlImagen)
    return img

def imagenLandMarks(rostroImagen):
    face_landmarks_list = face_recognition.face_landmarks (rostroImagen)
    return face_landmarks_list

def codificarArchivo(urlImagen):
    img = cargarImagen(urlImagen)
    face_encoding1 = face_recognition.face_encodings (img) [ 0 ]
    return face_encoding1

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
    
    
##################################### lectura de archivos  ####################################    
    
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
    #numeroPaquetes = b.count("],")
    #print("numero Paquetes: %d" %(numeroPaquetes))

    for paquete in b.split('],'):
        paquete = paquete.replace("[","")
        #cantidadDatosPaquete = paquete.count(",")
        #print("cantidad Datos Paquete: %d" %(cantidadDatosPaquete))
        
        if len(paquete)>10:   
            ListaDatosString = paquete.split(',')
            listaDatosFloat = [ float(i) for i in  ListaDatosString]  #convierto cada item de la cadena a float
            ArrayDatos = np.array(listaDatosFloat)
            matrixDatosRostros.append(ArrayDatos)   
    return matrixDatosRostros
    
from os import listdir
from os.path import isfile, join    
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

def ActualizarBaseDatos():
    known_face_encodings,known_face_names = listaDatos_Nombres()
    GuardarArchivosCodificados(known_face_encodings, known_face_names)
    

    
def QuienEs(ruta):
    nombre = "Sin Identificar"
    face_encoding3 = codificarArchivo(ruta)
    results = face_recognition.compare_faces (leerArrayDatos(), face_encoding3)
    if True in results:
        indice = results.index(True)
        nombre = leerArrayNombres()[indice]
    return nombre

def datosPersonas():
    datosPersonas = leerArrayDatos()
    return datosPersonas

def buscarPersonaEnBancoDatos(datosPersona, ruta):
    nombre = "Sin Identificar"
    face_encoding3 = codificarArchivo(ruta)
    results = face_recognition.compare_faces (datosPersona, face_encoding3)
    if True in results:
        indice = results.index(True)
        nombre = leerArrayNombres()[indice]
    return nombre

def compararDatosVsImagenActual(datosPersonas, EncodeActual, tolerancia=0.70):
    results = face_recognition.compare_faces (datosPersonas, EncodeActual, tolerancia)
    nombre = "Sin Identificar"
    if True in results:
        indice = results.index(True)
        nombre = leerArrayNombres()[indice]
    return nombre

def localizacionRostros(imagenCompleta):
    face_locations = face_recognition.face_locations(imagenCompleta)
    return face_locations
    
def codificarRostrosImagenCompleta(imagenCompleta, ubicacionRostros):
    face_encodings = face_recognition.face_encodings(imagenCompleta, ubicacionRostros)
    return face_encodings

def conteoRostrosImagenCompleta(ubicacionRostros):
    return len(ubicacionRostros)

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
    
       
    
    
print("Sistema Cargado y listo para reconocer Rostros")