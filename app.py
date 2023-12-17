from flask import Flask, render_template, jsonify, request
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['DATABASE'] = 'db/cookieclicker.db'
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    if not hasattr(app, 'contador_principal'):
        db = connect_db()
        cursor = db.cursor()
        cursor.execute('SELECT c1 FROM contadores')
        app.contador_principal = cursor.fetchone()[0]
        db.close()

@app.route('/aumentarContador', methods=['POST'])
def aumentar_contador():
    try:
        db = connect_db()
        cursor = db.cursor()

        
        cursor.execute('UPDATE contadores SET c1 = c1 + 1000')
        db.commit()

        
        cursor.execute('SELECT c1 FROM contadores')
        app.contador_principal = cursor.fetchone()[0]

        
        if app.contador_principal >= 9999:
            
            cursor.execute('UPDATE contadores SET c1 = c1 - 9990')
            db.commit()
            app.contador_principal -= 9900
            
            return jsonify({'success': True, 'message': '¡Ganaste! Se restaron 9900 puntos', 'contador_principal': app.contador_principal})

        db.close()

        return jsonify({'success': True, 'message': 'Contador aumentado con éxito', 'contador_principal': app.contador_principal})
    except Exception as e:
        return jsonify({'error': 'Error al aumentar el contador principal de cookies'})

@socketio.on('manejar_contador')
def manejar_contador(data):
    x = data['x']
    y = data['y']

    try:
        db = connect_db()
        cursor = db.cursor()

        
        cursor.execute('UPDATE contadores SET c1 = c1 + 20')

        db.commit()

        
        cursor.execute('SELECT c1 FROM contadores')
        app.contador_principal = cursor.fetchone()[0]

        db.close()

        
        socketio.emit('update_contador', {'contador_principal': app.contador_principal})

        
        emit('manejar_contador_confirmacion', {'success': True})
    except Exception as e:
        print(str(e))
        
        emit('manejar_contador_confirmacion', {'success': False})

@socketio.on('restar_contador')
def restar_contador(data):
    try:
        db = connect_db()
        cursor = db.cursor()

        
        cursor.execute('UPDATE contadores SET c1 = c1 - ?', (data['puntos'],))
        db.commit()

        
        cursor.execute('SELECT c1 FROM contadores')
        app.contador_principal = cursor.fetchone()[0]
        db.close()

        
        socketio.emit('update_contador', {'contador_principal': app.contador_principal})
    except Exception as e:
        print(str(e))

@app.route('/')
def index():
    try:
        return render_template('index.html', contador_principal=app.contador_principal)
    except Exception as e:
        return jsonify({'error': 'Error al obtener el contador principal de cookies'})

@app.route('/restarGalletas', methods=['POST'])
def restar_galletas():
    try:
        
        galletas_a_restar = 2000

       
        if app.contador_principal >= galletas_a_restar:
            db = connect_db()
            cursor = db.cursor()

           
            cursor.execute('UPDATE contadores SET c1 = c1 - ?', (galletas_a_restar,))
            db.commit()

            
            cursor.execute('SELECT c1 FROM contadores')
            app.contador_principal = cursor.fetchone()[0]
            db.close()

           
            socketio.emit('update_contador', {'contador_principal': app.contador_principal})

            return jsonify({'success': True, 'message': 'Galletas restadas con éxito'})
        else:
            return jsonify({'success': False, 'message': 'No hay suficientes galletas para restar'})
    except Exception as e:
        print(str(e))
        return jsonify({'success': False, 'message': 'Error al restar galletas'})

@app.route('/restarTripleClick', methods=['POST'])
def restar_triple_click():
    try:
        
        galletas_a_restar = 3500

        
        if app.contador_principal >= galletas_a_restar:
            db = connect_db()
            cursor = db.cursor()

            
            cursor.execute('UPDATE contadores SET c1 = c1 - ?', (galletas_a_restar,))
            db.commit()

            
            cursor.execute('SELECT c1 FROM contadores')
            app.contador_principal = cursor.fetchone()[0]
            db.close()

            
            socketio.emit('update_contador', {'contador_principal': app.contador_principal})

            return jsonify({'success': True, 'message': 'Galletas restadas por triple click'})
        else:
            return jsonify({'success': False, 'message': 'No hay suficientes galletas para restar por triple click'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al restar galletas por triple click'})

@app.route('/restablecerContador', methods=['POST'])
def restablecer_contador():
    try:
       
        db = connect_db()
        cursor = db.cursor()

        
        cursor.execute('SELECT c1 FROM contadores')
        contador_actual = cursor.fetchone()[0]

        if contador_actual <= 0:
            
            puntos_a_sumar = abs(contador_actual) + 100
            cursor.execute('UPDATE contadores SET c1 = ?', (puntos_a_sumar,))
            db.commit()

            
            cursor.execute('SELECT c1 FROM contadores')
            app.contador_principal = cursor.fetchone()[0]
            db.close()

            
            socketio.emit('update_contador', {'contador_principal': app.contador_principal})

            return jsonify({'success': True, 'message': 'Contador restablecido con éxito'})
        else:
            
            db.close()
            return jsonify({'success': False, 'message': 'El contador no es 0 o negativo, no es necesario restablecer'})
    except Exception as e:
        print(str(e))
        return jsonify({'success': False, 'message': 'Error al restablecer el contador'})

@app.route('/restarPuntosGanados', methods=['POST'])
def restar_puntos_ganados():
    try:
        db = connect_db()
        cursor = db.cursor()

        
        cursor.execute('UPDATE contadores SET c1 = c1 - 9999')
        db.commit()

        cursor.execute('SELECT c1 FROM contadores')
        app.contador_principal = cursor.fetchone()[0]
        db.close()

        return jsonify({'success': True, 'message': 'Se restaron 9900 puntos con éxito', 'contador_principal': app.contador_principal})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Error al restar 9900 puntos: ' + str(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
