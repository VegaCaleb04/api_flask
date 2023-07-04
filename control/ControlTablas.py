from control.ControlConexionPostgreSQL import *
from control.configBdPostgreSQL import *
class ControlTablas():
    def __init__(self):
        pass

    def obtenerListaGeoTablas(self,table_schema):
        listaGeoTablas=[]
        listaTablasBase=[]
        listaVistas=[]
        listaCampos=[]
        msg="ok"
        objControlConexion = ControlConexionPostgreSQL()
        comandoSql="SELECT table_name FROM information_schema.tables WHERE table_schema='{}' AND table_type='BASE TABLE';".format(table_schema)
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):         
                for fila in cursor:
                    listaTablasBase.append(fila[0])
                objControlConexion.cerrarBd() 
                for tabla in listaTablasBase:
                    listaCampos=self.obtenerListaCampos(tabla)
                    for campo in listaCampos:
                        if campo=='geom':
                            listaGeoTablas.append(tabla)
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)

        objControlConexion = ControlConexionPostgreSQL()
        comandoSql="SELECT table_name FROM information_schema.views WHERE table_schema='{}';".format(table_schema)
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):         
                for fila in cursor:
                    listaVistas.append(fila[0])
                objControlConexion.cerrarBd() 
                for tabla in listaVistas:
                    listaCampos=self.obtenerListaCampos(tabla)
                    for campo in listaCampos:
                        if campo=='geom':
                            listaGeoTablas.append(tabla)
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)

        return listaGeoTablas
 
    def obtenerListaTablas(self):
        pass
    def obtenerListaCampos(self,tabla):
        listaCampos=[]
        msg="ok"
        comandoSql="SELECT column_name	FROM information_schema.columns	WHERE table_name = '{}';".format(tabla)
        objControlConexion = ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):         
                for field in cursor:
                    listaCampos.append(field[0])
                objControlConexion.cerrarBd() 
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return listaCampos