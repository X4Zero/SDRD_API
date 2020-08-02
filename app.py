from flask import Flask, request, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)

# Mysql connection
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'sdrd'

# settings
app.secret_key = 'mysecretkey'

mysql = MySQL(app)


@app.route('/')
def index():
    return 'SDRD - API'

# Sección paciente
@app.route('/pacientes',methods=['POST'])
def registrar_paciente():
    if request.method=='POST':
        print(request.json)
        id = request.json['idpaciente']
        nombres = request.json['nombres']
        apellidos = request.json['apellidos']
        dni = request.json['dni']
        direccion = request.json['direccion']
        telefono = request.json['telefono']

        # Se registra paciente
        try:

            cur = mysql.connection.cursor()
            query_insert = "INSERT INTO paciente VALUES ('{}','{}','{}','{}','{}','{}');".format(id,nombres,apellidos,dni,direccion,telefono)
            print("REGISTRAR-PACIENTE")
            print('query_insert: ',query_insert)
            cur.execute(query_insert)
            mysql.connection.commit()

        except Exception as e:
            print(e)
            return jsonify({"mensaje": "Algo salió mal"})

        return jsonify({'mensaje':'Se ha registrado con éxito el paciente'})

@app.route('/pacientes/<id>', methods=['PUT'])
def actualizar_paciente(id):
    
    cur = mysql.connection.cursor()
    query_select = "SELECT * FROM paciente WHERE idpaciente ='{}'".format(id)
    print("ACTUALIZAR-PACIENTE")
    print("query_select: ",query_select)
    cur.execute(query_select)

    paciente = cur.fetchone()
    if not paciente :
        return jsonify({"mensaje":"paciente no encontrado"})
    else:
        try:
            datos=[]
            query = """UPDATE paciente
                SET """
            
            # print(request.json)
            # print(type(request.json))

            for key, val in request.json.items():
                query+= key + "=%s,"
                datos.append(val)
            query = query[:-1]
            query += " WHERE idpaciente= %s"

            datos.append(id)
            datos_tupla = tuple(datos)

            # print("query:",query)
            # print("datos:",datos_tupla)
            cur = mysql.connection.cursor()
            cur.execute(query, datos_tupla)
        
            mysql.connection.commit()

            return jsonify({"mensaje": "Paciente actualizado satisfactoriamente"})
        except Exception as e:
            print(e)
            return jsonify({"mensaje": "Algo salió mal"})

@app.route('/pacientes')
def obtener_pacientes():
    cur = mysql.connection.cursor()
    query_select='SELECT * FROM paciente'
    print("REGISTRAR-PACIENTE")
    print('query_select: ',query_select)
    cur.execute(query_select)
    pacientes_obtenidos  =  cur.fetchall()
    pacientes_respuesta = []
    for paciente in pacientes_obtenidos:
        paciente_dict = {"idpaciente":paciente[0], "nombres":paciente[1], "apellidos":paciente[2], "dni":paciente[3], "direccion":paciente[4], "telefono":paciente[5]}
        pacientes_respuesta.append(paciente_dict)

    return jsonify({'pacientes':pacientes_respuesta})

@app.route('/pacientes/<id>')
def obtener_paciente(id):
    cur = mysql.connection.cursor()
    query_select = "SELECT * FROM paciente WHERE idpaciente = '{}'".format(id)
    print("OBTENER-PACIENTE")
    print('query_select: ',query_select)
    cur.execute(query_select)

    paciente = cur.fetchone()
    if paciente :
        return jsonify({"paciente":{"idpaciente":paciente[0], "nombres":paciente[1], "apellidos":paciente[2], "dni":paciente[3], "direccion":paciente[4], "telefono":paciente[5]}})
    else:
        return jsonify({"mensaje":"paciente no encontrado"})

@app.route('/pacientes/busqueda/<texto>')
def buscar_pacientes(texto):

    texto = texto.strip()
    print(texto)

    cur = mysql.connection.cursor()
    query_select = "SELECT * FROM paciente WHERE nombres LIKE '%" +texto +"%' OR apellidos LIKE '%"+texto+"%' OR idpaciente LIKE '%"+texto+"%';"
    print("BUSCAR-PACIENTES")
    print('query_select: ',query_select)
    cur.execute(query_select)
    pacientes_obtenidos  =  cur.fetchall()
    pacientes_respuesta = []
    # print(pacientes_obtenidos)
    if pacientes_obtenidos:
        for paciente in pacientes_obtenidos:
            paciente_dict = {"idpaciente":paciente[0], "nombres":paciente[1], "apellidos":paciente[2], "dni":paciente[3], "direccion":paciente[4], "telefono":paciente[5]}
            pacientes_respuesta.append(paciente_dict)

        return jsonify({'pacientes':pacientes_respuesta})
    else:
        return jsonify({'mensaje':'No se encontraron pacientes que coincidan con {}'.format(texto)})
# Fin sección paciente

# Sección diagnostico
@app.route('/diagnosticos',methods=['POST'])
def registrar_diagnostico():
    if request.method=='POST':
        print("REGISTRAR-DIAGNOSTICO")
        # print(request.json)

        rutaimagen = request.json['rutaimagen']
        diagnostico = request.json['diagnostico']
        # fecha = request.json['fecha']
        observaciones = request.json['observaciones']
        idpaciente = request.json['idpaciente']
        idusuario = request.json['idusuario']

        # Se registra paciente
        try:

            cur = mysql.connection.cursor()
            query_insert = "INSERT INTO diagnostico (rutaimagen,diagnostico,fecha,observaciones,paciente_idpaciente,usuario_idusuario) VALUES ('{}','{}',SYSDATE(),'{}','{}',{});".format(
                rutaimagen,diagnostico,observaciones,idpaciente,idusuario)
            print('query_insert: ',query_insert)
            cur.execute(query_insert)
            mysql.connection.commit()

        except Exception as e:
            print(e)
            return jsonify({"mensaje": "Algo salió mal"})

        return jsonify({'mensaje':'Se ha registrado con éxito el diagnóstico'})

@app.route('/diagnosticos')
def obtener_diagnosticos():
    cur = mysql.connection.cursor()
    query_select='SELECT * FROM diagnostico'
    print("OBTENER-DIAGNOSTICOS")
    print('query_select: ',query_select)
    cur.execute(query_select)
    diagnosticos_obtenidos  =  cur.fetchall()
    diagnosticos_respuesta = []
    for diagnostico in diagnosticos_obtenidos:
        diagnostico_dict = {"iddiagnostico":diagnostico[0], "rutaimagen":diagnostico[1], "diagnostico":diagnostico[2], "fecha":diagnostico[3], "observaciones":diagnostico[4], "idpaciente":diagnostico[5], "idusuario":diagnostico[6]}
        diagnosticos_respuesta.append(diagnostico_dict)

    return jsonify({'diagnosticos':diagnosticos_respuesta})

@app.route('/diagnosticos/<id>')
def obtener_diagnostico(id):
    cur = mysql.connection.cursor()
    query_select = "SELECT * FROM diagnostico WHERE iddiagnostico = '{}'".format(id)
    print("OBTENER-DIAGNOSTICO")
    print('query_select: ',query_select)
    cur.execute(query_select)

    diagnostico = cur.fetchone()
    if diagnostico :
        return jsonify({"diagnostico":{"iddiagnostico":diagnostico[0], "rutaimagen":diagnostico[1], "diagnostico":diagnostico[2], "fecha":diagnostico[3], "observaciones":diagnostico[4], "idpaciente":diagnostico[5], "idusuario":diagnostico[6]}})
    else:
        return jsonify({"mensaje":"diagnostico no encontrado"})

@app.route('/diagnosticos/paciente/<idpaciente>')
def obtener_diagnosticos_paciente(idpaciente):
    cur = mysql.connection.cursor()
    query_select="SELECT * FROM diagnostico WHERE paciente_idpaciente = '{}'".format(idpaciente)
    print("OBTENER-DIAGNOSTICOS-PACIENTE")
    print('query_select: ',query_select)
    cur.execute(query_select)
    diagnosticos_obtenidos  =  cur.fetchall()
    diagnosticos_respuesta = []
    for diagnostico in diagnosticos_obtenidos:
        diagnostico_dict = {"iddiagnostico":diagnostico[0], "rutaimagen":diagnostico[1], "diagnostico":diagnostico[2], "fecha":diagnostico[3], "observaciones":diagnostico[4], "idpaciente":diagnostico[5], "idusuario":diagnostico[6]}
        diagnosticos_respuesta.append(diagnostico_dict)

    return jsonify({'diagnosticos':diagnosticos_respuesta})

# Fin sección diagnostico

if __name__ == '__main__':
    app.run(port=5000, debug=True)