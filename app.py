from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)

#Rutas de aplicacion
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    
    #Convertir datos en diccionario
    insertObjet = []
    columNames = [column[0] for column in cursor.description]
    for record in  myresult:
        insertObjet.append(dict(zip(columNames, record)))
    cursor.close()

    return render_template('index.html', data=insertObjet)

#Ruta para guardar ususrios en la base de datos
@app.route('/user', methods=['POST'])
def addUser():
    #Obtener datos del formulario
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if username and name and password:
        #Guardar datos en la base de datos
        cursor = db.database.cursor()
        sql =  "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

#ruta para eliminar usurios
@app.route('/delete/<int:id>')
def  delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id = %s"
    data  = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

#ruta para ediar  usuarios
@app.route('/edit/<int:id>', methods=['POST'])
def edit(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    
    if username and name and password:
        #Guardar datos en la base de datos
        cursor = db.database.cursor()
        sql =  "UPDATE users SET username=%s, name=%s, password=%s WHERE id=%s"
        data = (username, name, password, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))
    
    
if __name__== '__main__':
    app.run(debug=True, port=5000)
    