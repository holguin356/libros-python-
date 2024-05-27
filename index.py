#importar la micro libreria flask, ctrl ñ pip install flask
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
#nombre del archivo de la base de datos
DATABASE = 'database.db'
#funcion creacion de la tabla
def create_table():
        conn = sqlite3.connect(DATABASE)
        #agregar un objeto, para interactuar con la sentencia sql
        cursor = conn.cursor()
        cursor.execute(''' 
                       CREATE TABLE IF NOT EXISTS libros(
                               id INTEGER PRIMARY KEY AUTOINCREMENT,
                               titulo TEXT,
                               autor TEXT
                       )
                       ''')
        #guardar en base de datos los cambios
        conn.commit()
        #cerrar la conexion
        conn.close()
#llamar la funcion
create_table()
@app.route('/')
def mostrar_libros():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    conn.close()
    return render_template('libro.html', libros=libros)

@app.route('/agregar_libro', methods = ['POST'])
def agregar_libro():
        titulo = request.form["titulo"]
        autor = request.form['autor']
        conn = sqlite3.connect(DATABASE)
        #agregar un objeto, para interactuar con la sentencia sql
        cursor = conn.cursor()
        cursor.execute('INSERT INTO libros (titulo,autor) VALUES (?,?)',(titulo, autor))
        conn.commit()
        conn.close()
        return redirect('/')

#ruta editar libro
@app.route('/editar_libro/<int:id>', methods = ['GET'])
def editar_libro(id):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, titulo, autor FROM libros WHERE id = ?", (id,))
        libro = cursor.fetchone()
        conn.close()
        return render_template('editar_libro.html', libro = libro)

#actualizar libro
@app.route('/editar_libro/<int:id>', methods = ['POST'])
def actualizar_libro(id):
        #se obtiene los datos del formulario
        titulo = request.form['titulo']
        autor = request.form['autor']
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("UPDATE libros SET titulo = ?, autor = ? WHERE id = ?", (titulo, autor, id))
        conn.commit()
        conn.close()
        return redirect(url_for('mostrar_libros'))
        
#Eliminar
@app.route('/eliminar_libro/<int:id>')
def eliminar_libro(id):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM libros WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        return redirect(url_for('mostrar_libros'))
#segunda seccion se ingresa a otra pagina http://127.0.0.1:5000/about
@app.route('/about')
def about():
        return render_template('about.html')
    
if __name__ == '__main__':
        app.run(debug=True)