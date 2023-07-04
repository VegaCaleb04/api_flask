from control.ControlConexionPostgreSQL import *
from control.configBdPostgreSQL import *
from modelo.RolUsuario import *
class ControlRolUsuario():
    def __init__(self,objRolUsuario):
        self.objRolUsuario = objRolUsuario

    def guardar(self):
        msg="ok"
        fkEma = self.objRolUsuario.getFkEmail()
        fkIdR = self.objRolUsuario.getFkIdRol()       
        comandoSql = "INSERT INTO rol_usuario(fkEmail,fkIdRol) VALUES ('{}',{})".format(fkEma,fkIdR)
        print("comandoSql=",comandoSql)
        objControlConexion = ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)       
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                msg=objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return msg

    def consultarRoles_por_EmailUsuario(self):
        msg="ok"
        matRolUsuario = []
        fkEma= self.objRolUsuario.getFkEmail()
        comandoSql = "SELECT rol.id,rol.nombre FROM rol INNER JOIN rol_usuario ON rol.id=rol_usuario.fkIdRol WHERE rol_usuario.fkEmail='{}'".format(fkEma)
        objControlConexion = ControlConexionPostgreSQL()
        msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0): 
                for i in range(cursor.rowcount):
                    matRolUsuario.append([])
                    for j in range(2):
                        matRolUsuario[i].append('')
                i=0
                for fila in cursor:        
                    matRolUsuario[i][0]=fila[0]
                    matRolUsuario[i][1]=fila[1]
                    i+=1
            objControlConexion.cerrarBd()
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
        print(msg)
        return matRolUsuario
    
    def borrarTodosEmailUsuario(self):
        msg = "ok"
        fkEma= self.objRolUsuario.getFkEmail() 
        comandoSql = "DELETE FROM rol_usuario WHERE fkEmail='{}'".format(fkEma)
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