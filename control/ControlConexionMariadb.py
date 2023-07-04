import mariadb
class ControlConexionMariadb():
    def __init__(self):
        self.conexion=None
        self.cursor = None
        self.listaConsulta=None
        self.mensaje="ok"
    def abrirBd(self,user,password,host,port,db):
        try:
            print(user,password,host,port,db)
            self.conexion =  mariadb.connect(
                user=user,
                password=password,
                host=host,
                port=port,
                database=db)
            self.cursor = self.conexion.cursor()
        except mariadb.Error as err:
             self.mensaje="Something went wrong: {}".format(err)
        except Exception as objExecption:
            self.mensaje="Something went wrong: {}".format(objExecption)
        print(self.mensaje)
        return self.mensaje
    def cerrarBd(self):
        try:
            self.cursor.close()
            self.conexion.close()
        except mariadb.Error as err:
             self.mensaje="Something went wrong: {}".format(err)
        except Exception as objExecption:
            self.mensaje="Something went wrong: {}".format(objExecption)
        print(self.mensaje)
        return self.mensaje
    def ejecutarComandoSql(self,comandoSql):
        try:
            self.cursor.execute(comandoSql)
            self.conexion.commit()
        except mariadb.Error as err:
             self.mensaje="Something went wrong: {}".format(err)
        except Exception as objExecption:
            self.mensaje="Something went wrong: {}".format(objExecption)
        print(self.mensaje)
        return  self.cursor