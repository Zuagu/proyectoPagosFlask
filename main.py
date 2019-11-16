from flask import Flask
from flask import request
from flask import render_template, json
from flask import jsonify
import csv
import sqlite3
import os
import xlrd
import datetime
import mysql.connector
#============================================================
app = Flask(__name__)
#============================================================
#============================================================
# modulo de login
@app.route('/')
@app.route('/index')
def index():
	return render_template('usuarios_call.html')
#============================================================
# modulo de login
@app.route('/usuarios_call', methods=['POST'])
def usuarios_call():
	con_call_center = mysql.connector.connect(
		host="192.168.0.6",
		user="root",
		passwd="Arcade2019",
		database="arcade_call"
	)
	miCursor = con_call_center.cursor()
	# mi_conexion = sqlite3.connect("base_Aplicacion")
	# miCursor = mi_conexion.cursor()
	# miCursor.execute("select * from usuarios_call")
	miCursor.execute('''select 
	id,
    nombre,
	nombre_puesto(id_puesto),
	DATE_FORMAT(date(fecha_alta), '%Y-%m-%d'),
    celular,
    ifnull(nombre_usuario_alias(id_jefe_inmediato),''),
    if(f_active = 1, 'ACTIVO', if(f_active=2, 'BAJA DEFINITIVA', 'INACTIVO')),
	alias,
    email,
	id_sucursal,
	id_puesto,
    id_jefe_inmediato,
	f_active,
    telefono,
    if(sexo = 'H','Masculino','Femenino'),
	sexo,
    if(f_administrativo = 1,'Administrativo','Operativo'),
	f_administrativo,
    if(id_sucursal = 1,'Monterrey','Puebla'),
	DATE_FORMAT(date(fecha_nacimiento), '%Y-%m-%d'),
	acta,
	ife,
	nss,
	curp,
	comp_est,
	comp_dom,
	cartas,
	fotos,
	infonavit,
	rfc,
	nombre_horario(id_horario),
	suspencion
    from arcade_usuarios where f_active = 1;''')
	myResult = miCursor.fetchall()
	return jsonify(myResult)
#============================================================
# modulo de Acceso Denegado
@app.route('/accedo_denegado')
def accedo_denegado():
	return render_template('AccDene.html')
#============================================================
# modulo Carucel
@app.route('/carrusel')
def carrusel():
	return render_template('carrusel.html')
# modulo de registro
#============================================================
@app.route('/registro')
def resgistro():
	return render_template('Registro.html')
#============================================================
# pagina de inicio
@app.route('/inicio')
def inicio():
	return render_template('inicio.html')
#============================================================
# Pagina de crear Tabla
@app.route('/create')
def create():
	conect_Base_datos()
	return "Tabla Creada"
#============================================================
# pagina de lista de usuarios
@app.route('/usuarios')
def usuarios():
	return render_template('usuarios.html')


@app.route('/tabla_usuarios', methods=['POST'])
def tabla_usuarios():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("SELECT * from usuarios;")
	resultado = mi_cursor.fetchall()
	return json.dumps(resultado)


@app.route('/insert_usuarios_js', methods=['POST'])
def insert_usuarios_js():
	datos_ingre = request.form['d_insert']
	print(datos_ingre)
	datos = insert_usuario(datos_ingre)
	return datos
def insert_usuario(datos):
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("insert into usuarios(nombre) values('"+datos+"')")
	mi_conexion.commit()
	mi_cursor.close()
	return 'Exitoso'

#============================================================
# validar usuario
@app.route('/identificador', methods=['POST'])
def identificador():
	nombre = request.form['user']
	password = request.form['pass']
	result = autenticar_usuario(nombre, password)
	print(result)

	if result == True:
		return 'inicio'
	else:
		return 'accedo_denegado'

#============================================================
@app.route('/reporte-base', methods=['POST'])
def reporte_base(): 
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("SELECT count(cuenta) as num, id_asignacion, id_region, region, asignacion from base_general group by id_asignacion;")
	
	resultado = mi_cursor.fetchall()
	return jsonify(resultado)
#============================================================
@app.route('/actualizar-base', methods=['POST'])
def actualizar_base(): 
	
	mensaje = datosBaseGeneral = consultaUpdateBaseGeneralLocal()
	print(datosBaseGeneral.__len__())
	insetDataDb(datosBaseGeneral)

	return str(mensaje) + " Base Genral Local Actualizada"
#============================================================
@app.route('/limpiar-base', methods=['POST'])
def limpiar_base(): 
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("delete from base_general")
	mi_conexion.commit()
	mi_conexion.close()
	
	return "Base General Limpiada"
#============================================================
@app.route('/bas')
def base():
	# conect_Base_datos()
	# datos = leerCsv()
	datosBaseGeneral = consultaUpdateBaseGeneralLocal()
	print(datosBaseGeneral.__len__())
	#insetDataDb(datos)

	return "Base Genral Local Actualizada"
# Leer csv
def leerCsv():
	with open("static/files/base-general.csv") as File:
		datos = []
		obtener_datos = csv.reader(File, delimiter=',', quotechar='\n', quoting=csv.QUOTE_MINIMAL)
		i=0
		for row in obtener_datos:
			datos.append(row)
			i = i + 1
	return datos

def consultaUpdateBaseGeneralLocal():
	print("Entrando a base de datos Sicsa")
	con_call_center = mysql.connector.connect(
		host="192.168.0.6",
		user="root",
		passwd="Arcade2019",
		database="arcade_call" 
	)
	miCursor = con_call_center.cursor()
	miCursor.execute("select columna1, id_asignacion, id_region, nombre_region(id_region), nombre_asignacion(id_asignacion)   from arcade_basegeneral where f_active = 1")
	# miCursor.execute("select * from arcade_pagos where fecha_aplicacion between '"+fecha_min+"' and  '"+fecha_max+"' ;")
	myResult = miCursor.fetchall()
	return myResult


def insetDataDb(datos):
	print(len(datos))
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.executemany("insert into base_general(cuenta, id_asignacion, id_region, region, asignacion) values(?,?,?,?,?)",datos)
	mi_conexion.commit()
	mi_conexion.close()
	return "datos Ingresados"

def insetPagosDb(datos_csv):
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.executemany("insert into pagos_temporal(cuenta, fecha_pago, origen, importe, forma, status, fecha_aplicacion) values(?,?,?,?,?,?,?)", datos_csv)
	mi_conexion.commit()
	mi_conexion.close()
	return "datos Ingresados"


def insetPagosExistentes(datos):
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.executemany('''insert into pagos_cargados(
		id_cliente,
		id_region,
		id_asignacion,
		cuenta, 
		fecha_pago, 
		origen, 
		importe, 
		forma, 
		status, 
		fecha_aplicacion,
		f_gestionado,
		cadenaunica
		) 
		values(?,?,?,?,?,?,?,?,?,?,?,?)''', datos)

	# mi_cursor.executemany('''insert into usuarios_call(
	# 	id,
	# 	nombre,
	# 	id_sucursal,
	# 	id_puesto,
	# 	fecha_alta,
	# 	telefono,
	# 	celular,
	# 	id_jefe_inmediato,
	# 	f_active,
	# 	alias,
	# 	sexo,
	# 	email,
	# 	f_administrativo,
	# 	fecha_nacimiento
	# 	) 
	# 	values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', datos)
	mi_conexion.commit()
	mi_conexion.close()
	return "datos Ingresados"


def updateIdentificarCuentas():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute('''   
		UPDATE pagos_temporal
		SET 
		id_cliente = 1,
		id_asignacion = (SELECT id_asignacion FROM base_general where cuenta = pagos_temporal.cuenta),
		id_region = (SELECT id_region FROM base_general where cuenta = pagos_temporal.cuenta);
	''')
	mi_conexion.commit()
	mi_conexion.close()
	return "Cuentas Identificadas"

def identificarPagosExistentes():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute('''
		SELECT cuenta, cadenaunica from pagos_temporal;
	''')
	resultado = mi_cursor.fetchall()

	for row in resultado:
		mi_cursor.execute("UPDATE pagos_temporal set existe = (select count(id_pago) from pagos_cargados where cadenaunica = '"+ str(row[1]) +"' ) where cuenta = "+ str(row[0]) +";")
		#mi_cursor.execute("UPDATE pagos_temporal set existe = (select count(cuenta) where cadenaunica = '"+row[0]+"' ) where cuenta = "+row[1]+";")
	mi_conexion.commit()
	mi_conexion.close()
	return "Se Actulizaron pagos Identificados"
	

def conect_Base_datos():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	# mi_cursor.execute('''CREATE TABLE usuarios ( 
	# 	id INTEGER PRIMARY KEY AUTOINCREMENT, 
	# 	nombre VARCHAR(100), 
	# 	usuario VARCHAR(100), 
	# 	password VARCHAR(50), 
	# 	categoria VARCHAR(50) 
	# 	)''')
	# mi_cursor.execute('''CREATE TABLE pagos_temporal ( 
	# 	id_pago INTEGER PRIMARY KEY AUTOINCREMENT, 
    #     id_cliente INTEGER,
    #     id_region INTEGER,
    #     id_asignacion INTEGER,
    #     cuenta INTEGER,
    #     fecha_pago VARCHAR(100),
    #     origen VARCHAR(100),
    #     importe VARCHAR(15),
    #     forma VARCHAR(100),
    #     status VARCHAR(100),
    #     fecha_aplicacion VARCHAR(100),
    #     f_gestionado VARCHAR(100),
    #     cadenaunica VARCHAR(100),
	# 	existe VARCHAR(100)
	# 	)''')
	mi_cursor.execute('''CREATE TABLE usuarios_call ( 
		id INTEGER PRIMARY KEY,
		nombre VARCHAR(100),
		id_sucursal INTEGER,
		id_puesto INTEGER,
		fecha_alta VARCHAR(100),
		telefono VARCHAR(100),
		celular VARCHAR(100),
		id_jefe_inmediato INTEGER,
		f_active INTEGER,
		alias VARCHAR(100),
		sexo VARCHAR(100),
		email VARCHAR(100),
		f_administrativo INTEGER,
		fecha_nacimiento VARCHAR(100)
	)''')
	mi_conexion.commit()
	mi_cursor.close()

	# mi_cursor.execute('''CREATE TABLE base_general ( 
	# 	id_cuenta INTEGER PRIMARY KEY AUTOINCREMENT, 
 #        cuenta INTEGER,
 #        id_asignacion INTEGER,
 #        id_region INTEGER,
 #        region VARCHAR(100),
 #        asignacion VARCHAR(100)
	# 	)''')
#============================================================
@app.route('/registrar_usuario', methods=['POST'])
def registrar_usuario():
	nombre = request.form['nombre']
	usuario = request.form['usuario']
	password = request.form['pass']
	categoria = request.form['categoria']
	
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()

	mi_cursor.execute("insert into usuarios values( NULL,'"+nombre+"','"+usuario+"','"+password+"','"+categoria+"')")
	mi_conexion.commit()
	mi_cursor.close()

	return "datos ingresados"
#============================================================
@app.route('/sms')
def sms():
	return render_template('mensaje-subir.html')

@app.route('/procesar-Archivos')
def procesar_Archivos():
	cargar_pagos()
	return render_template('mensaje-subir.html')


@app.route('/subir')
def subir():
	return render_template('subir.html')

@app.route('/subir-archivos', methods=['GET', 'POST'])
def subirArchivo():
	subirArchivos = request.files.getlist("file[]")
	#print(subirArchivos[0])
	# f = request.files['file']
	folder = os.path.realpath(__file__).replace('\\','/').split('/')[0:-1]
	for f in subirArchivos:
		f.save('/'.join(folder) + '/static/Archivos_Pagos/' + f.filename)

	return render_template('mensaje-subir.html') 

@app.route('/ver-contenido-carpeta', methods=['POST'])
def ver_contenido_carpeta():
	carpeta = request.form['carpeta']
	print(carpeta)
	contenido_carpeta = os.listdir("static/" + carpeta)
	return jsonify(contenido_carpeta)

#============================================================ Subir pagos
@app.route('/pagos')
def pagos():
	return render_template('tabla-pagos.html')

@app.route('/ver-pagos-cargados', methods=['POST'])
def ver_pagos_cargados():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("SELECT * from pagos_temporal order by fecha_aplicacion")
	resultado = mi_cursor.fetchall()

	return jsonify(resultado)
## eliminar pagos
@app.route('/eliminar-pagos', methods=['POST'])
def eliminar_pagos():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("delete from pagos_temporal;")
	#resultado = mi_cursor.fetchall()
	mi_conexion.commit()
	mi_cursor.close()
	return "si"

@app.route('/eliminar-pagos-cargados', methods=['POST'])
def eliminar_pagos_cargados():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("delete from pagos_cargados;")
	#resultado = mi_cursor.fetchall()
	mi_conexion.commit()
	mi_cursor.close()
	return "si"

## identificar pagos
@app.route('/identificar-pagos', methods=['POST'])
def identificar_pagos():
	ress = identificarPagosExistentes()
	return jsonify(ress)

## generar cadena unica
@app.route('/cadenaunica', methods=['POST'])
def cadenaunica():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute(
		"update pagos_temporal set cadenaunica = (cuenta || fecha_aplicacion || importe || forma || status), f_gestionado = 0 ;")
	
	mi_conexion.commit()
	mi_cursor.close()
	return "Cadena Unica Generada"

@app.route('/pagos-nuevos', methods=['POST'])
def pagos_nuevos():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("SELECT * from pagos_temporal where existe = 0 ;")
	
	myResult = mi_cursor.fetchall()
	return jsonify(myResult)

@app.route('/eliminar-files-pagos', methods=['POST'])
def eliminar_files_pagos():
	archivos_exitentes = os.listdir("static/Archivos_Pagos")
	archivos = []
	for x in archivos_exitentes:
		archivos.append(x)
		os.remove("static/Archivos_Pagos/"+x)

	return jsonify(archivos)

@app.route('/cargar-pagos', methods=['POST'])
def cargar_pagos():
	## Codigo para obtener el nombre de los archivos en la carpeta
	archivos_cargados = os.listdir("static/Archivos_Pagos")
	lista_de_archivos = []
	for x in archivos_cargados:
		lista_de_archivos.append(x)
	## cogigo sacar datos de los pagos de los archivos xls
	datos_pagos = []
	print(lista_de_archivos)
	for archivo in lista_de_archivos:
		try:
			datos_archivo = xlrd.open_workbook("static/Archivos_Pagos/" + archivo)
			datos_libro = datos_archivo.sheet_by_index(0)
			cant_filas = datos_libro.nrows
			cant_columnas = datos_libro.ncols
			j = 0
			identificador = datos_libro.cell_value(11, 0)
			for i in range(cant_filas):
				lista_interna=[]
				if datos_libro.cell_value(i, j) == identificador:
					for j in range(cant_columnas):
						if j != 0:
							if j == 2 or j == 7:
								lista_interna.append( datetime.datetime.strptime( datos_libro.cell_value(i, j), "%d/%m/%Y").strftime("%Y-%m-%d") )
							else:
								lista_interna.append(datos_libro.cell_value(i, j))
				j=0
				if len(lista_interna) != 0:
					datos_pagos.append(lista_interna)	
		except :
			print("No se encontro el Archivo: " + archivo)

	## inserta los pagos a la tabla temporal
	ress = insetPagosDb(datos_pagos)
	## identifica los pagos cargados
	updateIdentificarCuentas() 
	## cadena unica
	cadenaunica()
	## llenar la tabla de pagos cargados
	obtener_pagosBaseSicsa()
	## identificar los pagos de que ya existen 
	identificarPagosExistentes()
	## eliminar los pagos existentes

	## subir pagos no existentes

	# gestionar pagos nuevos

	## limpiar las dos tablas

	return ress


def obtener_fecha(tipo):
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	if tipo == "min":
		mi_cursor.execute("SELECT min(fecha_aplicacion) as maxf FROM pagos_temporal;")
	else:
		mi_cursor.execute("SELECT max(fecha_aplicacion) as maxf FROM pagos_temporal;")
	
	resultado = mi_cursor.fetchall()
	return resultado[0][0]

@app.route('/obtener-pagos-baseSicsa', methods=['POST'])
def obtener_pagosBaseSicsa():

	fecha_min = obtener_fecha("min")
	fecha_max = obtener_fecha("max")
	print("Entrando a base de datos Sicsa")
	con_call_center = mysql.connector.connect(
		host="192.168.0.6",
		user="root",
		passwd="Arcade2019",
		database="arcade_call" 
	)
	miCursor = con_call_center.cursor()
	miCursor.execute("select id_cliente, id_region, id_asignacion, cuenta, DATE_FORMAT(fecha_pago, '%Y-%m-%d') as fecha_pago, origen, importe, forma, status, DATE_FORMAT(fecha_aplicacion, '%Y-%m-%d') as fecha_aplicacion, f_gestionado, cadenaunica from arcade_pagos where fecha_aplicacion between '"+fecha_min+"' and  '"+fecha_max+"';")
	# miCursor.execute("select * from arcade_pagos where fecha_aplicacion between '"+fecha_min+"' and  '"+fecha_max+"' ;")
	myResult = miCursor.fetchall()
	pagos_exist =[]
	for cell in myResult:
		pagos_exist.append(cell)
	
	insetPagosExistentes(pagos_exist)

	return jsonify(pagos_exist)

@app.route('/reporte-pagos-cagados', methods=['POST'])
def reporte_pagos_cagados():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("select count(id_pago) as cantidad, id_region, id_asignacion from pagos_cargados group by id_asignacion;")
	resultado = mi_cursor.fetchall()
	return jsonify(resultado)

@app.route('/reporte-pagos', methods=['POST'])
def reporte_pagos():
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("select count(id_pago) as cantidad, id_region, id_asignacion from pagos_temporal group by id_asignacion;")
	resultado = mi_cursor.fetchall()
	return jsonify(resultado)

#============================================================
def autenticar_usuario(user, passw):
	mi_conexion = sqlite3.connect("base_Aplicacion")
	mi_cursor = mi_conexion.cursor()
	mi_cursor.execute("select * from usuarios where usuario = '"+user+"' ")
	resultado = mi_cursor.fetchall()
	print(resultado.__len__())

	if resultado.__len__() == 0:
		return False
	else:
		if passw == resultado[0][3]:
			return True
		else:
			return False

#============================================================

#============================================================

#============================================================

#============================================================

#============================================================

if __name__ == '__main__':
  app.run(debug = True, port = 9600 )
