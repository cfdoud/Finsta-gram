from flask import Flask, render_template, request
import json
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String
# Test 3
#uwu
app = Flask(__name__)
students_engine = create_engine('sqlite:///students.db', echo = True)
#classes_engine = create_engine('sqlite:///classes.db', echo = True)
students_meta = MetaData()
#classes_meta = MetaData()


students = Table(
   'students', students_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('classes', String), 
   Column('permission', Integer), 
   Column('username', String), 
   Column('password', String), 
)
#classes = Table(
#   'students', classes_meta, 
#   Column('id', Integer, primary_key = True), 
#   Column('name', String), 
#   Column('grade', Integer), 
#)
students_meta.create_all(students_engine)
#  classes_meta.create_all(classes_engine)




@app.route('/')
def home():
    return render_template('index.html')

@app.route('/student', methods = ['PASS'])
def studPull():
    student_connection = students_engine.connect()
    if (request.method == 'PASS'):
        added = request.data
        added = added.decode()
        added = json.loads(added)
        addedU = str(added['username'])
        addedP = str(added['password'])
        print(addedU)

        #s = students.select(students.c.password).where(students.c.username.equals(addedU))
        s = "SELECT password FROM students WHERE username='" + addedU + "'"
        result = student_connection.execute(s)
        row = str(result.fetchone())
        row = row[2:-3]
        student_connection.close() 
        if (addedP == row): return "true"
        else: return "false"




"""
@app.route('/data/<student>', methods = ['GET', 'DELETE', 'PUT'])
def studPull(student):
    conn = engine.connect()
    if(request.method == 'GET'):
        data = json.loads('{"Filler": 85}')
        del data["Filler"]
        s = students.select().where(students.c.name == student)
        result = conn.execute(s)
        for row in result:
            string = str(row)
            got = '{"' + string[string.index(',')+3:string.index(',', string.index(',')+1)-1] + '": ' + string[string.index(',', string.index(',')+1)+2:string.index(')')] + '}'
            got = json.loads(got)
            data.update(got)
        conn.close()
        return data
    if(request.method == 'DELETE'):
        deleted = '{"' + student + '": "removed"}'
        deleted = json.loads(deleted)
        rem = students.delete().where(students.c.name == student)
        conn.execute(rem)
        conn.close()
        return deleted
    if(request.method == 'PUT'):
        added = request.data
        added = added.decode()
        added = json.loads(added)
        addedG = str(added['grade'])
        rep = students.update().where(students.c.name == student).values(grade = addedG)
        conn.execute(rep)
        conn.close()
        return added

@app.route('/data', methods = ['GET', 'POST'])
def genPull():
    conn = engine.connect()
    if(request.method == 'GET'):
        data = json.loads('{"Filler": 85}')
        del data["Filler"]
        s = students.select()
        result = conn.execute(s)
        for row in result:
            string = str(row)
            got = '{"' + string[string.index(',')+3:string.index(',', string.index(',')+1)-1] + '": ' + string[string.index(',', string.index(',')+1)+2:string.index(')')] + '}'
            got = json.loads(got)
            data.update(got)
        conn.close()
        return data
    if(request.method == 'POST'):
        added = request.data
        added = added.decode()
        added = json.loads(added)
        addedN = str(added['name'])
        addedG = str(added['grade'])
        added = '{"' + addedN + '": "' + addedG + '"}'
        added = json.loads(added)

        ins = students.insert().values(name = addedN, grade = addedG)
        conn.execute(ins)
        conn.close()
        return added
"""

if __name__ == '__main__':
    app.run()