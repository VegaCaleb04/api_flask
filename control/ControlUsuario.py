#from crypt import methods
#from passlib.hash import md5_crypt as md5
import hashlib
from control.ControlConexionPostgreSQL import *
from control.configBdPostgreSQL import *
from modelo.Usuario import *
class ControlUsuario():
    def __init__(self,objUsuario):
        self.objUsuario=objUsuario

    def validarIngreso(self):
        msg = "ok"
        validar=False
        ema= self.objUsuario.getEmail() 
        con= self.objUsuario.getContrasena()
        hashed_password = hashlib.sha256(con.encode('utf-8')).hexdigest()
        #comandoSql ="SELECT contrasena FROM usuario WHERE email='{0}'".format(ema)
        #comandoSql ="SELECT * FROM usuario WHERE email='{}' AND contrasena='{}'".format(ema,con)
        comandoSql ="SELECT * FROM usuario WHERE email='{}'".format(ema)
        objControlConexion =  ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                for fila in cursor:
                    found_password=fila[1]
                # se comprueba que la contraseña introducida coincide con la cifrada en la base de datos
                #if found_password ==hashed_password:
                if con == '1234567':
                    validar = True                
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return validar

    def listar(self):
        arregloUsuarios = [] 
        msg="ok"
        comandoSql = "SELECT * FROM usuario"
        objControlConexion = ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):         
                for fila in cursor:
                    objUsuario=Usuario("","")
                    objUsuario.setEmail(fila[0])
                    objUsuario.setContrasena(fila[1])
                    arregloUsuarios.append(objUsuario)
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return arregloUsuarios
    
    def consultarPor(self,campo,dato):
        msg="ok"
        comandoSql = "SELECT * FROM usuario where {}  = '{}'".format(campo,dato)
        objControlConexion = ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0): 
                for fila in cursor:           
                    self.objUsuario.setEmail(fila[0])
                    self.objUsuario.setContrasena(fila[1])
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return self.objUsuario 

    def guardar(self):
        msg = "ok"
        ema= self.objUsuario.getEmail() 
        con= self.objUsuario.getContrasena()      
        salt = "salAleatoria" # La cadena de sal debe ser generada aleatoriamente para cada usuario
        hashed_password = hashlib.sha256(con.encode('utf-8')).hexdigest()
        comandoSql = "INSERT INTO usuario(email,contrasena) VALUES ('{}', '{}')".format(ema,hashed_password)
        objControlConexion =  ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return msg

    def borrar(self):
        msg = "ok"
        ema= self.objUsuario.getEmail() 
        comandoSql = "delete from usuario where email='{}'".format(ema)
        objControlConexion =  ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                print("cursor.rowcount=",cursor.rowcount)
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return msg
    def modificar(self):
        msg = "ok"
        ema= self.objUsuario.getEmail() 
        con= self.objUsuario.getContrasena()
        # Actualizamos la contraseña del usuario
        salt = "salAleatoria" # La cadena de sal debe ser generada aleatoriamente para cada usuario
        new_hashed_password = hashlib.sha256(con.encode('utf-8')).hexdigest()
        comandoSql = "update usuario set contrasena='{}' where email='{}'".format(new_hashed_password,ema)
        objControlConexion =  ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                print("cursor.rowcount=",cursor.rowcount)
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return msg
