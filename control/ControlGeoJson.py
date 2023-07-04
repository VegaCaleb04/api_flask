from control.ControlConexionPostgreSQL import *
from control.configBdPostgreSQL import *
class ControlGeoJson():
    def __init__(self):
        self.msg="ok"
    def obtenerGeoJson(self,geoTabla,campo):
        comandoSql =" SELECT row_to_json(fc) FROM ( SELECT 'FeatureCollection' As type, array_to_json(array_agg(f)) As features FROM (SELECT 'Feature' As type, ST_AsGeoJSON(lg.geom)::json As geometry, row_to_json(lp) As properties FROM public.{0} As lg INNER JOIN (SELECT * FROM public.{1}) As lp ON lg.{2} = lp.{3}) As f ) As fc;".format(geoTabla,geoTabla,campo,campo)
        objControlConexion = ControlConexionPostgreSQL()
        self.msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
        cursor = objControlConexion.ejecutarComandoSql(comandoSql)
        try:
            if (cursor.rowcount> 0):
                textoGeoJson=""
                for fila in cursor:           
                    textoGeoJson=str(fila[0])
            objControlConexion.cerrarBd()
        except Exception as objException:
            self.msg="Algo salió mal: {}".format(objException)
        print("En obtenerGeoJson retorna: ",self.msg)
        return textoGeoJson