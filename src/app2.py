
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from flask_cors import CORS

from config import config

app = Flask(__name__)

CORS(app)

con = MySQL(app)


@app.route("/maestros", methods=['GET'])
def lista_maestros():
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM maestros"
        cursor.execute(sql)
        datos = cursor.fetchall()

        maestros = []
        for fila in datos:
            maestro = {
                "idmaestro": fila[0],
                "nombre": fila[1],
                "apaterno": fila[2],
                "amaterno": fila[3],
                "correo": fila[4]
            }
            maestros.append(maestro)

        return jsonify({
            'maestros': maestros,
            'mensaje': 'Lista de maestros',
            'exito': True
        })

    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})


def leer_maestro_bd(idmaestro):
    try:
        cursor = con.connection.cursor()
        sql = "SELECT * FROM maestros WHERE idmaestro = %s"
        cursor.execute(sql, (idmaestro,))
        datos = cursor.fetchone()

        if datos is not None:
            maestro = {
                "idmaestro": datos[0],
                "nombre": datos[1],
                "apaterno": datos[2],
                "amaterno": datos[3],
                "correo": datos[4]
            }
            return maestro
        else:
            return None

    except Exception as ex:
        raise ex


@app.route("/maestros/<idmaestro>", methods=['GET'])
def leer_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro is not None:
            return jsonify({
                'maestro': maestro,
                'mensaje': 'Maestro encontrado',
                'exito': True
            })
        else:
            return jsonify({
                'maestro': None,
                'mensaje': 'Maestro no encontrado',
                'exito': False
            })

    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})


@app.route("/maestros", methods=['POST'])
def registra_maestro():
    try:
        datos = request.json

        cursor = con.connection.cursor()
        sql = """
            INSERT INTO maestros (nombre, apaterno, amaterno, correo)
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (
            datos['nombre'],
            datos['apaterno'],
            datos['amaterno'],
            datos['correo']
        ))
        con.connection.commit()

        return jsonify({
            'mensaje': 'Maestro registrado correctamente',
            'exito': True
        })

    except Exception as ex:
        return jsonify({"message": "error {}".format(ex), 'exito': False})


@app.route("/maestros/<idmaestro>", methods=['PUT'])
def actualizar_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro is not None:
            datos = request.json
            cursor = con.connection.cursor()

            sql = """
                UPDATE maestros
                SET nombre = %s, apaterno = %s,
                    amaterno = %s, correo = %s
                WHERE idmaestro = %s
            """
            cursor.execute(sql, (
                datos['nombre'],
                datos['apaterno'],
                datos['amaterno'],
                datos['correo'],
                idmaestro
            ))
            con.connection.commit()

            return jsonify({
                'mensaje': 'Maestro actualizado',
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': 'Maestro no actualizado: no encontrado',
                'exito': False
            })

    except Exception as ex:
        return jsonify({"message": "Error {}".format(ex), 'exito': False})


def pagina_no_encontrada(error):
    return "<h1>Página no encontrada</h1>", 404


@app.route("/maestros/<idmaestro>", methods=['DELETE'])
def eliminar_maestro(idmaestro):
    try:
        maestro = leer_maestro_bd(idmaestro)

        if maestro is not None:
            cursor = con.connection.cursor()
            sql = "DELETE FROM maestros WHERE idmaestro = %s"
            cursor.execute(sql, (idmaestro,))
            con.connection.commit()

            return jsonify({
                'mensaje': 'Maestro eliminado',
                'exito': True
            })
        else:
            return jsonify({
                'mensaje': 'Maestro no encontrado',
                'exito': False
            })

    except Exception as ex:
        return jsonify({"message": "Error {}".format(ex), 'exito': False})


if __name__ == "__main__":
    app.config.from_object(config['development'])
    app.register_error_handler(404, pagina_no_encontrada)
    app.run(host='0.0.0.0', port=5001, debug=True)
