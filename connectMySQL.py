import mysql.connector

db_call_celter = mysql.connector.connect(
    host="192.168.0.6",
    user="root",
    passwd="Arcade2019",
    database="arcade_call"
)

myCursor = db_call_celter.cursor()

myCursor.execute("select id, nombre from arcade_usuarios where f_active = 1;");

usuarios = []

myResult = myCursor.fetchall()

for x in myResult:
    persona=[]
    persona.append(x[0])
    persona.append(x[1])
    usuarios.append(persona)

print(usuarios)
