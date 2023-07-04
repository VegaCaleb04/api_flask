
from flask import Flask, render_template, request, url_for, redirect, jsonify,session,escape
from werkzeug.utils import secure_filename
from datetime import datetime
#from gevent.pywsgi import WSGIServer
from modelo.Usuario import *
from modelo.Rol import *
from modelo.RolUsuario import *
from control.ControlUsuario import *
from control.ControlRol import *
from control.ControlRolUsuario import *
from control.ControlConexionPostgreSQL import *
from control.ControlArchivos import *
from control.ControlGeoJson import *
from control.ControlTablas import *
app = Flask(__name__)
app.secret_key='secret_key'
@app.route('/', methods = ['GET', 'POST']) 
def index():
    ema=""
    con=""
    bot=""
    print("entró a index con ",request.method, " ",datetime.now())
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        ema=escape(request.form['txtEmail'])
        con=escape(request.form['txtContrasena'])
        bot=escape(request.form['btnLogin'])
        if bot=='Login':
            validar=False
            objUsuario= Usuario(ema,con)
            objControlUsuario=ControlUsuario(objUsuario)
            validar=objControlUsuario.validarIngreso()
            if validar:
                objRolUsuario=RolUsuario(ema,0)
                objControlRolUsuario= ControlRolUsuario(objRolUsuario)
                matRolesDelUsuario = objControlRolUsuario.consultarRoles_por_EmailUsuario()
                session['ema']=escape(ema)
                session['matRolesDelUsuario']=matRolesDelUsuario
                return render_template('/menu.html',ema=ema)
            else:
                return render_template('/index.html')
        else:
            return render_template('/index.html')
    else:
        return render_template('/index.html')

@app.route('/menu',methods = ['GET', 'POST'])
def menu():
    if 'ema' in session:
        return render_template('/menu.html')
    return redirect(url_for('index'))

@app.route('/vistaUsuarios', methods = ['GET', 'POST'])
def vistaUsuarios():
    arregloUsuarios=[]
    usuario = {
    'email': '',
    'contrasena': ''
    }
    if 'ema' in session:
        permisoParaEntrar=False
        matRolesDelUsuario = session.get('matRolesDelUsuario', [])
        i=0
        while i < len(matRolesDelUsuario):
            if matRolesDelUsuario[i][1] == "admin":
                permisoParaEntrar = True
            i+=1
        if permisoParaEntrar==False:
            return redirect(url_for('index')) 
    else:
        return redirect(url_for('index'))  
    msg="ok"
    objControlUsuario=ControlUsuario(None)
    arregloUsuarios=objControlUsuario.listar()
    objControlRol=ControlRol(None)
    arregloRoles=objControlRol.listar()
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=escape(request.form['bt'])
        ema=escape(request.form['txtEmail'])
        con=escape(request.form['txtContrasena']) 
        ListBox1=request.form.getlist('ListBox1')                                    
        usuario = {
            'email': ema,
            'contrasena': con
        }
        if bt=='Guardar':
            try:
                objUsuario= Usuario(ema,con)
                objControlUsuario= ControlUsuario(objUsuario)
                objControlUsuario.guardar()
                arregloRolUsuario=[]
                if len(ListBox1) != 0:
                    for i in range(len(ListBox1)):
                        id = ListBox1[i].split(";")[0]
                        objRolUsuario = RolUsuario(ema, id)
                        objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                        objControlRolUsuario.guardar() #Guarda los datos de las claves foráneas en la tabla intermedia tblrol_usuario
                else:
                    id=1 #di=1 es invitado
                    objRolUsuario = RolUsuario(ema, id)
                    arregloRolUsuario[0] = objRolUsuario
                    objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                    objControlRolUsuario.guardar()           
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect(url_for('vistaUsuarios'))			          
        elif bt=='Consultar':
            try:
                objUsuario=  Usuario(ema,"");
                objControlUsuario= ControlUsuario(objUsuario);
                objUsuario=objControlUsuario.consultarPor('email',ema)
                ema=objUsuario.getEmail()
                con=objUsuario.getContrasena()
                objRolUsuario = RolUsuario(ema, 0)
                objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                matRolesDelUsuario = objControlRolUsuario.consultarRoles_por_EmailUsuario()
                if matRolesDelUsuario==None:
                    matRolesDelUsuario=[[1,'invitado']]
                usuario = {
                    'email': ema,
                    'contrasena': con
                }                 
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
                print(msg)
            return render_template('/vistaUsuarios.html',arregloUsuarios=arregloUsuarios,usuario=usuario,matRolesDelUsuario=matRolesDelUsuario,arregloRoles=arregloRoles)
        elif bt=='Modificar':
            try:
                #modifica en la tabla Usuario
                #nota: Para esto debería hacerse en un procedimiento almacenado con manejo de transacciones
			    #1. modifica en la tabla Usuario
                objUsuario= Usuario(ema,con)
                objControlUsuario= ControlUsuario(objUsuario)
                objControlUsuario.modificar()
                #2. borra los registros asociados del usuario en la tabla intermedia
                objRolUsuario = RolUsuario(ema, 0)
                objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                objControlRolUsuario.borrarTodosEmailUsuario()
                #3. guarda de nuevo en la tabla intermedia
                arregloRolUsuario=[]
                if len(ListBox1) != 0:
                    i=0
                    while i < len(ListBox1):
                        id = ListBox1[i].split(";")[0]
                        objRolUsuario = RolUsuario(ema, id)
                        objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                        objControlRolUsuario.guardar() #Guarda los datos de las claves foráneas en la tabla intermedia tblrol_usuario
                        i+=1
                else:
                    objRolUsuario = RolUsuario(ema, 1)
                    arregloRolUsuario[0] = objRolUsuario
                    objControlRolUsuario = ControlRolUsuario(objRolUsuario)
                    objControlRolUsuario.guardar() #Guarda los datos de las claves foráneas en la tabla intermedia tblrol_usuario

            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
                print(msg)
            return redirect('/vistaUsuarios')			
        elif bt=='Borrar':
            try:
                objUsuario=  Usuario(ema,"")
                objControlUsuario= ControlUsuario(objUsuario)
                #en este caso considero que está bien aplicar ON DELETE CASCADE 
		        #al contraint de clave foránea con_fkEmail de la tabla rol_usuario
                objControlUsuario.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaUsuarios')			                                
    return render_template('/vistaUsuarios.html',arregloUsuarios=arregloUsuarios,usuario=usuario)

@app.route('/vistaRoles', methods = ['GET', 'POST'])
def vistaRoles():
    arregloRoles=[]
    rol = {
    'id': '',
    'nombre': ''
    }
    if 'ema' in session:
        permisoParaEntrar=False
        matRolesDelUsuario = session.get('matRolesDelUsuario', [])
        i=0
        while i < len(matRolesDelUsuario):
            if matRolesDelUsuario[i][1] == "admin":
                permisoParaEntrar = True
            i+=1
        if permisoParaEntrar==False:
            return redirect(url_for('index')) 
    else:
        return redirect(url_for('index'))  
    msg="ok"
    objControlRol=ControlRol(None)
    arregloRoles=objControlRol.listar()
    objControlRol=ControlRol(None)
    arregloRoles=objControlRol.listar()
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        bt=escape(request.form['bt'])
        id=escape(request.form['txtId']),
        nombre=escape(request.form['txtNombre'])                                       
        rol = {
        'id': id,
        'nombre': nombre
        }
        if bt=='Guardar':
            try:
                objRol= Rol(id,nombre)
                objControlRol= ControlRol(objRol)
                objControlRol.guardar()
                arregloRolUsuario=[]        
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect(url_for('vistaRoles'))			          
        elif bt=='Consultar':
            try:
                objRol= Rol(id,"")
                objControlRol= ControlRol(objRol)
                objRol=objControlRol.consultar()
                nombre=objRol.getNombre()
                rol = {
                    'id': id,
                    'nombre': nombre
                }               
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
                print(msg)
            return render_template('/vistaRoles.html',arregloRoles=arregloRoles,rol=rol)
        elif bt=='Modificar':
            try:
                objRol= Rol(id,nombre)
                objControlRol= ControlRol(objRol)
                objRol=objControlRol.modificar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
                print(msg)
            return redirect('/vistaRoles')			
        elif bt=='Borrar':
            try:
                objRol= Rol(id,"")
                objControlRol= ControlRol(objRol)
                objRol=objControlRol.borrar()
            except Exception as objException:
                msg="Algo salió mal: {}".format(objException)
            return redirect('/vistaRoles')			                                
    return render_template('/vistaRoles.html',arregloRoles=arregloRoles,rol=rol)
@app.route('/geovisor', methods = ['GET', 'POST'])
def geovisor():
    if 'ema' in session:
        permisoParaEntrar=False
        matRolesDelUsuario = session.get('matRolesDelUsuario', [])
        i=0
        while i < len(matRolesDelUsuario):
            if matRolesDelUsuario[i][1] == "invitado":
                permisoParaEntrar = True
            i+=1
        if permisoParaEntrar==False:
            return redirect(url_for('index')) 
    else:
        return redirect(url_for('index')) 
    
    bt=""
    txtAreaConsulta=""
    cargado=""
    ruta=""
    listacampos=[]
    objControlTablas=ControlTablas();
    listaGeoTablas=objControlTablas.obtenerListaGeoTablas('public')
    #request.form.getlist('selTablas')=listaGeoTablas[0]
    listaCampos=objControlTablas.obtenerListaCampos(listaGeoTablas[0])
    consultaSQLparaSelect=f"DROP VIEW IF EXISTS vista; CREATE VIEW vista as SELECT * FROM {listaGeoTablas[0]};"
    if request.method == 'POST':
        bt=escape(request.form['boton'])
        txtAreaConsulta=escape(request.form['txtAreaConsulta'])
        file = request.files['selecArchivo']
        if bt=='Consultar':           
            objControlGeoJson = ControlGeoJson()
            objControlArchivos1 = ControlArchivos("")
            objControlArchivos1.borrarUnArchivo("static/data/consulta.js")
            objControlArchivos = ControlArchivos("static/data/consulta.js")
            objControlArchivos.crearArchivoBorrarContenido()
            objControlArchivos.escribirUnaLineaYAlFrente("var consulta=")           
            textoGeoJson=objControlGeoJson.obtenerGeoJson(request.form.get('selTablas'),'gid')
            
            objControlArchivos.escribirUnaLineaYDebajo(textoGeoJson)
            objControlArchivos.cerrarArchivo()

            consultaSQLparaSelect=f"DROP VIEW IF EXISTS vista; CREATE VIEW vista as SELECT * FROM {request.form.get('selTablas')};"
            listaCampos=objControlTablas.obtenerListaCampos(request.form.get('selTablas'))
            
        if bt=='Cargararchivo':
            pass
            """
            nomReal=secure_filename(file.filename)
            file.save("static/data/"+nomReal)
            objControlGeoJson = ControlGeoJson()           
                   
            objControlArchivos3 = ControlArchivos("")
            objControlArchivos3.borrarUnArchivo("static/data/tmp.json")         
            objControlArchivos3.borrarUnArchivo("static/data/cargado.js")                        
            objControlArchivos3.renombrarUnArchivo("static/data/"+nomReal,"static/data/tmp.json")
            
            objControlArchivos1 = ControlArchivos("static/data/tmp.json")
            objControlArchivos2 = ControlArchivos("static/data/cargado.js")  
            objControlArchivos1.abrirArchivoLecturaEscritura()
            objControlArchivos2.crearArchivoBorrarContenido()                      
            objControlArchivos2.escribirUnaLineaYAlFrente('var cargado=')
            linea=objControlArchivos1.leerUnaLinea()
            i=1
            while linea:
                objControlArchivos2.escribirUnaLineaYAlFrente(linea)
                print(i,end=" ")
                linea=objControlArchivos1.leerUnaLinea()
                i+=1
                
            
            objControlArchivos1.cerrarArchivo()
            objControlArchivos2.cerrarArchivo()   
            objControlArchivos3.borrarUnArchivo("static/data/tmp.json")
            """            
        if bt=='CrearVista': 
            objControlConexion = ControlConexionPostgreSQL()
            comandoSql="SELECT table_name FROM information_schema.tables WHERE table_schema='{}' AND table_type='BASE TABLE';".format('public')
            msg=objControlConexion.abrirBd(usua,passw,serv,port,bdat)
            objControlConexion.ejecutarComandoSql(txtAreaConsulta)
            objControlConexion.cerrarBd()    
                 
            objControlGeoJson = ControlGeoJson()
            objControlArchivos1 = ControlArchivos("")
            objControlArchivos1.borrarUnArchivo("static/data/vista.js")
            
            objControlArchivos = ControlArchivos("static/data/vista.js")
            objControlArchivos.crearArchivoBorrarContenido()
            objControlArchivos.escribirUnaLineaYAlFrente("var vista=")  
                     
            textoGeoJson=objControlGeoJson.obtenerGeoJson('vista','gid')         
           
            objControlArchivos.escribirUnaLineaYDebajo(textoGeoJson)
            objControlArchivos.cerrarArchivo()

            consultaSQLparaSelect=f"DROP VIEW IF EXISTS vista; CREATE VIEW vista as SELECT * FROM {request.form.get('selTablas')};"
            listaCampos=objControlTablas.obtenerListaCampos(request.form.get('selTablas'))

    return render_template('/geovisor.html',listaGeoTablas=listaGeoTablas,listaCampos=listaCampos,consultaSQLparaSelect=consultaSQLparaSelect)
@app.route('/cerrarSesion')
def cerrarSesion():
    session.clear()
    return redirect(url_for('index'))
@app.before_request
def before_request():
    #print("Entró a before_request ",datetime.now())
    pass

@app.after_request
def after_request(response):
    #print("Entró a after_request ",datetime.now())
    #print("response = ",response)
    return response

@app.route('/consultaGeoJson')
def consultaGeoJson():
    objArchivo= ControlArchivos('consulta.js')
    objArchivo.borrarUnArchivo('consulta.js')
    objArchivo.abrirArchivoEscritura()
    objArchivo.escribirUnaLineaYAlFrente("var consulta = ")
    objControlGeoJson= ControlGeoJson()
    textoGeoJson=objControlGeoJson.obtenerGeoJson('comunas_medellin','nom_com')
    objArchivo.escribirUnaLineaYAlFrente(textoGeoJson)
    objArchivo.cerrarArchivo()
    #return textoGeoJson
    #return render_template('geovisor/geovisor.html')
    return "Ok"


def query_string():
    print("query_string ",datetime.now())
    print(request)
    print(request.args)
    print(request.args.get('a'))
    print(request.args.get('b'))
    return "Ok"

def pagina_no_encontrada(error):
    # return render_template('404.html'), 404
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.add_url_rule('/query_string', view_func=query_string)
    app.register_error_handler(404, pagina_no_encontrada)
    # Debug/Development
    #app.run(debug=True, host="127.0.0.1", port="5000", threaded=True)
    app.run(debug=True, host="127.0.0.1", port="5000")
    # Production
    #http_server = WSGIServer(('', 5000), app)
    #http_server.serve_forever()