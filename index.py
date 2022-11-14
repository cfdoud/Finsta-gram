from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String


# Initializes app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "If yall can come up with a better secret key feel free, it's kinda important soooooooooooo"

# Initializes databases
students_engine = create_engine('sqlite:///students.db', echo = True)
classes_engine = create_engine('sqlite:///classes.db', echo = True)
junction_engine = create_engine('sqlite:///junction.db', echo = True)

students_meta = MetaData()
classes_meta = MetaData()
junction_meta = MetaData()

students = Table(
   'students', students_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String),
   Column('permission', Integer), 
   Column('username', String), 
   Column('password', Integer))

classes = Table(
   'classes', classes_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String), 
   Column('studentCount', Integer),
   Column('capacity', Integer),
   Column('time', String),
   Column('professor', String))
junction = Table(
   'junction', junction_meta, 
   Column('id', Integer, primary_key = True), 
   Column('student', Integer), 
   Column('class', Integer),
   Column('grade', Integer))

students_meta.create_all(students_engine)
classes_meta.create_all(classes_engine)
junction_meta.create_all(junction_engine)



# App responses to connections at various URLs

# Initialization at starting the program
@app.route('/')
def home():
    # Sets the current user to be null, displays login page
    session['user'] = "null"
    return render_template('index.html')


# This is where requests to /student are handled, PASS is used to authenticate users, LOGOUT to log the user out, CLASSES to pull class information for the current user
# and GET as what happens when you manually type the URL in.
@app.route('/student', methods = ['PASS', 'LOGOUT', 'CLASSES', 'GET', 'ADD', 'DROP'])
def studPassPull():
    if (request.method == 'PASS'):
        # Initializes connection to the students database
        student_connection = students_engine.connect()

        # Takes in username and password from the log-in page and assigns them to addedU and addedP
        added = request.data
        added = added.decode()
        added = json.loads(added)
        addedU = str(added['username'])
        addedP = added['password']

        # Finds password in the database (hashed) and assigns it to row
        s = "SELECT password FROM students WHERE username='" + addedU + "'"
        result = student_connection.execute(s)
        row = str(result.fetchone())

        # If the user is not in the database, row will be assigned to None, here that is handled
        if (row == "None"): 
            # Closes connection to student database
            student_connection.close() 
            # Returns failure message to page
            return "User not found"

        # Cleans the string with the password to only display the password, and displays the given username/password compared to the actual
        row = row[1:-2]
        print("Username: " + addedU + ", hashed password: " + str(row) + ", given: " + str(addedP))
        row = int(row)

        # If the password matches, the below is executed to login the user
        if (addedP == row): 
            # Finds the name of the user and assigns it to name
            s = "SELECT name FROM students WHERE username='" + addedU + "'"
            result = student_connection.execute(s)
            name = str(result.fetchone())
            # Finds the permission value of the user and assigns it to permission
            s = "SELECT permission FROM students WHERE username='" + addedU + "'"
            result = student_connection.execute(s)
            permission = str(result.fetchone())
            # Finds the student id of the user and assigns it to id
            s = "SELECT id FROM students WHERE username='" + addedU + "'"
            result = student_connection.execute(s)
            id = str(result.fetchone())
            # Closes connection to student database
            student_connection.close()
            # Saves the student's name, id, username, and permission value into the session
            session['user'] = addedU
            session['name'] = name[2:-3]
            session['permission'] = int(permission[1:-2])
            session['id'] = int(id[1: -2])

            # Returns success message to the page
            return "Successfully logged in; Hello " + session['name'] + "!"
        # The below is executed when the password is incorrect
        else: 
            # Closes connection to student database
            student_connection.close() 
            # Returns failure message to the page
            return "Incorrect password"
    if (request.method == 'LOGOUT'):
        # Removes current session data
        session['user'] = "null"
        session['name'] = "null"
        session['permission'] = -1
        session['id'] = -1
        # Returns to log-in page
        return render_template('index.html')
    if (request.method == 'GET'):
        # Returns to log-in page
        return redirect("http://127.0.0.1:5000/")
    if (request.method == 'CLASSES'):
        # Initializes connection to the junction database
        junction_connection = junction_engine.connect()
        # Pulls what classes the student is in from junction using their student id, assigns returned list to result
        s = "SELECT * FROM junction WHERE student='" + str(session['id']) + "'"
        result = junction_connection.execute(s)

        # Creates string returnedjson to store classes student is in along with their grade
        returnedjson = '{'
        # Iterates through returned list using parameter row for each line
        for row in result:
            # Converts the row of data to a string
            string = str(row)
            print(string)
            # Cuts out unnecessary portions of the data
            string = string[string.index(',')+3:]
            string = string[string.index(',')+2:]
            # Appends important part of data to returnedjson
            returnedjson += '"' + string[:string.index(',')] + '": "' + string[string.index(',')+2:-1] + '", '
        # Cleans up returnedjson
        returnedjson = returnedjson[:-2] + "}"
        print(returnedjson)
        # Closes connection to the junction database
        junction_connection.close() 

        # Converts returnedjson into a python dictionary
        returnedjson = json.loads(returnedjson)
        # Connects to classes database
        classes_connection = classes_engine.connect()

        # Creates string finaljson to store all information of the classes the student is in
        finaljson = '{'

        # Iterates through returnedjson, such that key is the class id for each class the student is in
        for key in returnedjson:
            # Pulls class data for the key/current class
            s = "SELECT * FROM classes WHERE id='" + key + "'"
            result = classes_connection.execute(s)
            # Appends class data to finaljson
            finaljson += '"' + str(result.fetchone()) + '": "'  + returnedjson[key] + '", '
        # Cleans up finaljson
        finaljson = finaljson[:-2] + "}"

        # Closes connection to classes database
        classes_connection.close()
        print(finaljson)

        # Return class information
        return finaljson
    if (request.method == 'DROP'):
        # Initializes connection to the junction database
        junction_connection = junction_engine.connect()
        
        removed = request.data
        removed = removed.decode()
        removed = json.loads(removed)
        removedClass = removed['classID']

        s = "DELETE FROM junction WHERE student='" + str(session['id']) + "' AND class=" + str(removedClass) + "'"
        result = junction_connection.execute(s)
        return("owo")
    if (request.method == 'ADD'):
        print("L")
        return("L")


# This is where requests for data for a specific student is handled, you can only 'GET' from here
@app.route('/student/<username>', methods = ['GET'])
def studPull(username):
    if (request.method == 'GET'):
        print("current user: " + session['user'])
        print("attempted user: " + username)
        # If the accessed user is the one currently logged in, redirect to their page, else redirect to the log-in page
        if (session['user'] == username):
            print("Permission: " + str(session['permission']))
            if (session['permission'] == 2): return render_template('adm.html')
            if (session['permission'] == 1): return render_template('teach.html')
            return render_template('stud.html')
        else: return redirect("http://127.0.0.1:5000/")

# Start the app
if __name__ == '__main__':
    app.run()