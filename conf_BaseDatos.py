import sqlite3
import mysql.connector
import json


def crear_tabla():
    myCon = sqlite3.connect("base_Aplicacion")
    myCursor = myCon.cursor()
    myCursor.execute('''
        create table nuevaBaseGeneral (
            id_cuenta INTEGER,
            cuenta INTEGER,
            id_region INTEGER,
            id_asignacion INTEGER,
            dias_anticipados INTEGER,
            a_gestionar FLOAT(11,2),
            fecha_inicio VARCHAR(20),
            fecha_fin VARCHAR(20),
            suma_pagos FLOAT(11,2)
        )
    ''')
    myCon.commit()
    myCursor.close()

def updateBaseGeneralLocal():
	myCon = mysql.connector.connect(
		host="192.168.0.6",
		user="root",
		passwd="Arcade2019",
		database="arcade_call" 
	)
	myCursor = myCon.cursor()
	myCursor.execute('''select  id_cuenta, columna1, id_region, id_asignacion, 3 as dias_anticipados, a_gestionar, DATE_FORMAT(fecha_inicio, '%Y-%m-%d'),  DATE_FORMAT(fecha_fin, '%Y-%m-%d'), pagos from arcade_basegeneral where f_active = 1 limit 10 ''')
	myResult = myCursor.fetchall()
	return myResult


def select_cuentas_pagos_nuevos():
    myCon = sqlite3.connect("base_Aplicacion")
    myCursor = myCon.cursor()
    myCursor.execute('''
        select cuenta from pagos_temporal where existe = 0;
    ''')
    cuentas = []
    myResult = myCursor.fetchall()
    for val in myResult:
        #print(val[0])
        cuentas.append(val[0])
    return cuentas


def updatenuevaBaseGeneral(valores):
    myCon = sqlite3.connect("base_Aplicacion")
    myCursor = myCon.cursor()
    myCursor.executemany('''
        insert into nuevaBaseGeneral (
            id_cuenta,
            cuenta,
            id_region,
            id_asignacion,
            dias_anticipados,
            a_gestionar,
            fecha_inicio,
            fecha_fin,
            suma_pagos
        ) values(?,?,?,?,?,?,?,?,?)
    ''', valores)
    myCon.commit()
    myCon.close()


resut_data =  updateBaseGeneralLocal()

updatenuevaBaseGeneral(resut_data)
