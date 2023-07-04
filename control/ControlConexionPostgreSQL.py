import psycopg2
class ControlConexionPostgreSQL():
    def __init__(self):
        self.conn=None
        self.cursor = None
        self.listaConsulta=None
        self.mensaje="ok"
    def abrirBd(self,user,password,host,port,db):
        try:
            self.conn =  psycopg2.connect(
                host=host, 
                database=db, 
                user=user, 
                password=password, 
                port=port)
            self.cursor = self.conn.cursor()
        except psycopg2.Error as objError:
                self.mensaje=objError.pgerror
                print(objError.pgerror)
        return self.mensaje
    
    def cerrarBd(self):
        try:
            #self.cursor.close()
            self.conn.close()
        except psycopg2.Error as objError:
                self.mensaje=objError.pgerror
                print(objError.pgerror)
        return self.mensaje
    
    def ejecutarComandoSql(self,comandoSql):
        try:
            self.cursor.execute(comandoSql)
            self.conn.commit()
        except psycopg2.Error as objError:
                self.mensaje=objError.pgerror
                print(objError.pgerror)
        return  self.cursor

    def obtenerListaTablas(self):
        msg="ok"
        sql="SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"
        cursor = self.ejecutarComandoSql(sql)
        listaTablas = []
        try:
            if (cursor.rowcount> 0):         
                for row in cursor:
                    listaTablas.append(row[0])
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return listaTablas

    def obtenerListaGeoTablas(self):
        msg="ok"
        sql="SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';";
        cursor = self.ejecutarComandoSql(sql)
        print(sql)
        listaGeoTablas = []
        try:
            print(cursor.rowcount,cursor)
            i=0
            if (cursor.rowcount> 0):         
                for row in cursor:
                    i=i+1
                    print(i,row)
                    listaCampos=self.obtenerListaCampos(row[0])
                    print(listaCampos)
                    for field in listaCampos:
                        print(field)
                        if field=='geom':
                            listaGeoTablas.append(row[0])
                            
            sql="SELECT table_name FROM information_schema.views WHERE table_schema='public';"
            cursor = self.ejecutarComandoSql(sql)
            print(sql)
            if (cursor.rowcount> 0):         
                    for row in cursor:
                        listaCampos=self.obtenerListaCampos(row[0])
                        print(listaCampos)
                        for field in listaCampos:
                            print(field)
                            if field=='geom':
                                listaGeoTablas.append(row[0])
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return listaGeoTablas
    
    def obtenerListaCampos(self,tabla):
        msg="ok"
        sql="SELECT column_name	FROM information_schema.columns	WHERE table_name = '{}';".format(tabla)
        cursor = self.ejecutarComandoSql(sql)
        listaCampos = []
        try:
            if (cursor.rowcount> 0):         
                for field in cursor:
                    listaCampos.append(field[0])
        except Exception as objException:
            msg="Algo salió mal: {}".format(objException)
            print(msg)
        return listaCampos