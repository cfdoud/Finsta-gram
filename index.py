from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String

#comment

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
students_engine = create_engine('sqlite:///students.db', echo = True)
classes_engine = create_engine('sqlite:///classes.db', echo = True)
junction_engine = create_engine('sqlite:///junction.db', echo = True)
students_meta = MetaData()
classes_meta = MetaData()
junction_meta = MetaData()

app.secret_key = "If yall can come up with a better secret key feel free, it's kinda important soooooooooooo"


students = Table(
   'students', students_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String),
   Column('permission', Integer), 
   Column('username', String), 
   Column('password', Integer), 
)
classes = Table(
   'classes', classes_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('studentCount', Integer),
   Column('capacity', Integer),
   Column('time', String),
   Column('professor', String)
)
junction = Table(
   'junction', junction_meta, 
   Column('id', Integer, primary_key = True), 
   Column('student', Integer), 
   Column('class', Integer),
   Column('grade', Integer),
)
students_meta.create_all(students_engine)
classes_meta.create_all(classes_engine)
junction_meta.create_all(junction_engine)


@app.route('/')
def home():
    session['user'] = "null"
    return render_template('index.html')



@app.route('/student', methods = ['PASS', 'LOGOUT', 'CLASSES'])
def studPassPull():
    if (request.method == 'PASS'):
        student_connection = students_engine.connect()
        added = request.data
        added = added.decode()
        added = json.loads(added)
        addedU = str(added['username'])
        addedP = added['password']

        s = "SELECT password FROM students WHERE username='" + addedU + "'"
        result = student_connection.execute(s)
        row = str(result.fetchone())
        if (row == "None"): 
            student_connection.close() 
            return "User not found"

        row = row[1:-2]
        print("Username: " + addedU + ", hashed password: " + str(row) + ", given: " + str(addedP))
        row = int(row)

        if (addedP == row): 
            s = "SELECT name FROM students WHERE username='" + addedU + "'"
            result = student_connection.execute(s)
            name = str(result.fetchone())
            s = "SELECT permission FROM students WHERE username='" + addedU + "'"
            result = student_connection.execute(s)
            permission = str(result.fetchone())
            s = "SELECT id FROM students WHERE username='" + addedU + "'"
            result = student_connection.execute(s)
            id = str(result.fetchone())
            student_connection.close()
            session['user'] = addedU
            session['name'] = name[2:-3]
            session['permission'] = int(permission[1:-2])
            session['id'] = int(id[1: -2])
            return "Successfully logged in; Hello " + session['name'] + "!"
        else: 
            student_connection.close() 
            return "Incorrect password"
    if (request.method == 'LOGOUT'):
        session['user'] = "null"
        return render_template('index.html')
    if (request.method == 'CLASSES'):
        junction_connection = junction_engine.connect()
        s = "SELECT * FROM junction WHERE student='" + str(session['id']) + "'"
        result = junction_connection.execute(s)
        returnedjson = '{'
        for row in result:
            string = str(row)
            print(string)
            string = string[string.index(',')+3:]
            string = string[string.index(',')+2:]
            returnedjson += '"' + string[:string.index(',')] + '": "' + string[string.index(',')+2:-1] + '", '
        returnedjson = returnedjson[:-2] + "}"
        print(returnedjson)
        junction_connection.close() 

        returnedjson = json.loads(returnedjson)
        classes_connection = classes_engine.connect()
        finaljson = '{'

        for key in returnedjson:
            s = "SELECT * FROM classes WHERE id='" + key + "'"
            result = classes_connection.execute(s)
            finaljson += '"' + str(result.fetchone()) + '": "'  + returnedjson[key] + '", '
        finaljson = finaljson[:-2] + "}"
        classes_connection.close()
        print(finaljson)
        return finaljson


@app.route('/student/<username>', methods = ['GET'])
def studPull(username):
    if (request.method == 'GET'):
        print("current user: " + session['user'])
        print("attempted user: " + username)
        if (session['user'] == username):
            print("Permission: " + str(session['permission']))
            if (session['permission'] == 2): return render_template('adm.html')
            if (session['permission'] == 1): return render_template('teach.html')
            return render_template('stud.html')
        else: return redirect("http://127.0.0.1:5000/")

if __name__ == '__main__':
    app.run()