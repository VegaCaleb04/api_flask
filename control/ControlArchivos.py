#https://www.tutorialspoint.com/python3/python_files_io.htm
##Por el tipo de acceso.
##'r' es el modo de lectura.
##'w' es un modo de escritura. En caso de existir un archivo, éste es sobreescrito.
##'a' es un modo de escritura. En caso de existir un archivo, comienza a escribir al final de éste.
##'x' es un modo de escritura para crear un nuevo archivo. En caso de que el archivo exista se emitirá un error de tipo FileExistsError.
##'+' es un modo de escritura/lectura.
import os
class ControlArchivos():
    def __init__(self,rutaYNombre):
        self.rutaYNombre =rutaYNombre
        self.f=None
        self.mensaje=""

    def crearArchivoBorrarContenido(self):
        try:
            if os.path.exists(self.rutaYNombre):
                self.f = open(self.rutaYNombre,'w+')#abre archivo para escritura. Borra todo
            else:
                self.f = open(self.rutaYNombre,'w+')#crea archivo para escritura.

        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje
    def abrirArchivoEscritura(self):
        try:
            if os.path.exists(self.rutaYNombre):
                self.f = open(self.rutaYNombre,'a+')#abre archivo para lectura escritura
            else:
                self.f = open(self.rutaYNombre,'a+')#crea archivo para lectura escritura
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje

    def abrirArchivoLecturaEscritura(self):
        try:
            if os.path.exists(self.rutaYNombre):
                self.f = open(self.rutaYNombre,'r+')#abre archivo para lectura escritura
            else:
                self.f = open(self.rutaYNombre,'a+')#crea archivo para lectura escritura
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje

    def cerrarArchivo(self):
        self.mensaje="ok"
        try:
            self.f.close()
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje

    def leerUnaLinea(self):
        self.mensaje="ok"
        lineaTexto=None
        try:
            lineaTexto = self.f.readline()
            if lineaTexto[-1] == '\n':
                lineaTexto=lineaTexto[:-1] #elimina el \n que está en la última posición
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
            return self.mensaje
        return lineaTexto

    def escribirUnaLineaYAlFrente(self,lineaTexto):
        self.mensaje="ok"
        try:
             self.f.writelines(lineaTexto)
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje

    def escribirUnaLineaYDebajo(self,lineaTexto):
        self.mensaje="ok"
        try:
             self.f.writelines(lineaTexto+"\n")
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje

    def crearCarpeta(self):
        pass

    def borrarUnArchivo(self,rutaYNombre):
        self.mensaje="ok"
        try:
            print("os.remove(rutaYNombre)=",rutaYNombre)
            os.remove(rutaYNombre)
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje
    
    def renombrarUnArchivo(self,rutaYNombreViejo,rutaYNombreNuevo):
        self.mensaje="ok"
        try:
            os.rename(rutaYNombreViejo, rutaYNombreNuevo)
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return self.mensaje

    def contarNumLineasArchivo(self):
        self.mensaje="ok"
        n=0
        try:
            LineaTexto=self.leerUnaLinea()
            while LineaTexto:
                n=n+1
                LineaTexto=self.leerUnaLinea()               
        except IOError as objIOError:
            self.mensaje= "Problemas con el archivo: Error #" + str(objIOError.errno) + " Mensaje : "+format(objIOError.strerror)
            print(self.mensaje)
        return n


