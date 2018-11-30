import os.path
import os
from shutil import copyfile

camaraOcupada = "temporal/camaraOcupada.txt"
temporalDatos = "temporal/nuevoDatos.csv"
temporalNombres = "temporal/nuevoNombres.csv"
temporalCopiando = "temporal/copiando.txt"
existeTemporales = "temporal/hayTemporales.txt"

def ExisteArchivo(url):
    return os.path.isfile(url)

def borrarArchivo(url):
    os.remove(url)
    
def crearArchivo(url):
    file = open(url,"w")
    file.write("Wisrovi.rodriguez@gmail.com")
    file.close()
    
def copiarArchivo(urlOrigen, urlDestino):
    copyfile(urlOrigen, urlDestino)
    
def procesoCopiarBaseDatos():
    ejecutado = False
    if ExisteArchivo(existeTemporales)==True:
        if ExisteArchivo(temporalCopiando)==True:
            print(">")
        else:
            print("Abriendo Archivos Temporales")
            archivoDatos = "pictures_encoded/data.csv"
            archivoNombres = "pictures_encoded/names.csv"
            if ExisteArchivo(temporalNombres)==True:
                if ExisteArchivo(temporalDatos)==True:
                    #existen los dos archivos
                    if ExisteArchivo(archivoDatos)==True:
                        borrarArchivo(archivoDatos)
                    if ExisteArchivo(archivoNombres)==True:
                        borrarArchivo(archivoNombres)
                    #copio archivos
                    print("copiando archivos temporales")
                    copiarArchivo(temporalNombres,archivoNombres)
                    copiarArchivo(temporalDatos,archivoDatos)
                    #borro temporales
                    borrarArchivo(temporalNombres)
                    borrarArchivo(temporalDatos)
                    #confirmo borrado temporales
                    if ExisteArchivo(temporalNombres)==True:
                        borrarArchivo(temporalNombres)
                    if ExisteArchivo(temporalDatos)==True:
                        borrarArchivo(temporalDatos)
                        
                    if ExisteArchivo(existeTemporales)==True:
                        borrarArchivo(existeTemporales)
                    if ExisteArchivo(temporalCopiando)==True:
                        borrarArchivo(temporalCopiando)
                    print("Cerrando archivos temporales")
                    ejecutado = True
                else:
                    print("no hay archivo de datos pero si de nombres")
            else:
                print("no hay archivo de nombres")
    return ejecutado
                    
