from flask import Flask, render_template, request, session, redirect, url_for, jsonify
import json
from sqlalchemy import create_engine, MetaData, Column, Table, Integer, String



# Initializes app
app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "If yall can come up with a better secret key feel free, it's kinda important soooooooooooo"



# Initializes databases
userdata_engine = create_engine('sqlite:///userdata.db', echo = True)
followingTable_engine = create_engine('sqlite:///followingTable.db', echo = True)
posts_engine = create_engine('sqlite:///posts.db', echo = True)
messages_engine = create_engine('sqlite:///messages.db', echo = True)

userdata_meta = MetaData()
followingTable_meta = MetaData()
posts_meta = MetaData()
messages_meta = MetaData()

userdata = Table(
   'userdata', userdata_meta, 
   Column('id', Integer, primary_key = True), 
   Column('name', String),
   Column('email', String), 
   Column('username', String), 
   Column('password', Integer),
   Column('bio', String),
   Column('profilePicture', String))

followingTable = Table(
   'followingTable', followingTable_meta, 
   Column('id', Integer, primary_key = True), 
   Column('user', Integer), 
   Column('following', Integer))

posts = Table(
   'posts', posts_meta, 
   Column('id', Integer, primary_key = True), 
   Column('user', Integer), 
   Column('message', String),
   Column('image', String))

messages = Table(
   'messages', messages_meta, 
   Column('id', Integer, primary_key = True), 
   Column('user', Integer), 
   Column('recipient', Integer),
   Column('message', String),
   Column('image', String))

userdata_meta.create_all(userdata_engine)
followingTable_meta.create_all(followingTable_engine)
posts_meta.create_all(posts_engine)
messages_meta.create_all(messages_engine)


# App responses to connections at various URLs

# Initialization at starting the program
@app.route('/')
def home():
    # Sets the current user to be null, displays login page
    session['username'] = "null"
    return render_template('index.html')



# This is where requests to /student are handled, PASS is used to authenticate users, LOGOUT to log the user out, CLASSES to pull class information for the current user
# and GET as what happens when you manually type the URL in.
@app.route('/userdata', methods = ['PASS', 'LOGOUT', 'CLASSES', 'ALLCLASSES', 'GET', 'ADD', 'DROP', 'GETNAME', 'GETPERM', 'CHANGEGRADE'])
def studPassPull():
    if (request.method == 'PASS'):
        # Initializes connection to the students database
        userdata_connection = userdata_engine.connect()

        # Takes in username and password from the log-in page and assigns them to addedU and addedP
        added = request.data
        added = added.decode()
        added = json.loads(added)
        addedU = str(added['username'])
        addedP = added['password']

        # Finds password in the database (hashed) and assigns it to row
        s = "SELECT password FROM userdata WHERE username='" + addedU + "'"
        result = userdata_connection.execute(s)
        row = str(result.fetchone())
        print(row)

        # If the user is not in the database, row will be assigned to None, here that is handled
        if (row == "None"): 
            # Closes connection to student database
            userdata_connection.close() 
            # Returns failure message to page
            return "User not found"

        # Cleans the string with the password to only display the password, and displays the given username/password compared to the actual
        row = row[1:-2]
        print("Username: " + addedU + ", hashed password: " + str(row) + ", given: " + str(addedP))
        row = int(row)

        # If the password matches, the below is executed to login the user
        if (addedP == row): 
            # Finds the name of the user and assigns it to name
            s = "SELECT name FROM userdata WHERE username='" + addedU + "'"
            result = userdata_connection.execute(s)
            name = str(result.fetchone())
            # Finds the profilePicture of the user and assigns it to profilePicture
            s = "SELECT profilePicture FROM userdata WHERE username='" + addedU + "'"
            result = userdata_connection.execute(s)
            profilePicture = str(result.fetchone())
            # Finds the id of the user and assigns it to id
            s = "SELECT id FROM userdata WHERE username='" + addedU + "'"
            result = userdata_connection.execute(s)
            id = str(result.fetchone())
            # Finds the email of the user and assigns it to email
            s = "SELECT id FROM userdata WHERE username='" + addedU + "'"
            result = userdata_connection.execute(s)
            email = str(result.fetchone())
            # Finds the email of the user and assigns it to email
            s = "SELECT bio FROM userdata WHERE username='" + addedU + "'"
            result = userdata_connection.execute(s)
            bio = str(result.fetchone())
            # Closes connection to student database
            userdata_connection.close()
            # Saves the student's name, id, username, and permission value into the session
            session['username'] = addedU
            session['name'] = name[2:-3]
            session['email'] = email[2:-3]
            session['bio'] = bio[2:-3]
            session['profilePicture'] = profilePicture[2:-3]
            session['id'] = int(id[1: -2])


            # Returns success message to the page
            return "Successfully logged in; Hello " + session['name'] + "!"
        # The below is executed when the password is incorrect
        else: 
            # Closes connection to student database
            userdata_connection.close() 
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
        classes_connection = classes_engine.connect()
        
        removed = request.data
        removed = removed.decode()
        removed = json.loads(removed)
        removedClass = removed['classID']
        removedStud = removed['studentID']


        s = "SELECT studentCount FROM classes WHERE id='" + str(removedClass) + "'"
        result = classes_connection.execute(s)
        studCount = str(result.fetchone())[1:-2]
        studCount = int(studCount) - 1

        s = classes.update().where(classes.c.id == removedClass).values(studentCount = studCount)
        result = classes_connection.execute(s)


        if (removedStud == -1): s = "DELETE FROM junction WHERE student='" + str(session['id']) + "' AND class='" + str(removedClass) + "'"
        else: s = "DELETE FROM junction WHERE student='" + str(removedStud) + "' AND class='" + str(removedClass) + "'"
        result = junction_connection.execute(s)
        junction_connection.close()


        return("owo")
    if (request.method == 'ADD'):
        junction_connection = junction_engine.connect()
        classes_connection = classes_engine.connect()
        print("test")
        
        added = request.data
        added = added.decode()
        added = json.loads(added)
        addedClass = added['classID']
        addedGrade = added['grade']
        addedStud = added['studentID']

        s = "SELECT capacity FROM classes WHERE id='" + str(addedClass) + "'"
        result = classes_connection.execute(s)
        capacity = str(result.fetchone())[1:-2]
        capacity = int(capacity)

        s = "SELECT studentCount FROM classes WHERE id='" + str(addedClass) + "'"
        result = classes_connection.execute(s)
        studCount = str(result.fetchone())[1:-2]
        studCount = int(studCount)
        if (capacity <= studCount): return ("failure")
        studCount = studCount + 1

        s = classes.update().where(classes.c.id == addedClass).values(studentCount = studCount)
        result = classes_connection.execute(s)

        if (addedStud == -1): s = "INSERT INTO junction (student, class, grade) VALUES ('" + str(session['id']) + "', '" + str(addedClass) + "', '" + str(addedGrade) + "')"
        else: s = "INSERT INTO junction (student, class, grade) VALUES ('" + str(addedStud) + "', '" + str(addedClass) + "', '" + str(addedGrade) + "')"
        result = junction_connection.execute(s)
        junction_connection.close()
        return("success")
    if (request.method == 'ALLCLASSES'):
        classes_connection = classes_engine.connect()
        junction_connection = junction_engine.connect()
        s = "SELECT * FROM classes"
        result = classes_connection.execute(s)

        returnedString = "{"
        for row in result:
            string = str(row)
            string = string[1:string.index(',')]
            t = "SELECT * FROM junction WHERE student='" + str(session['id']) + "' AND class='" + string + "'"
            t = junction_connection.execute(t)
            t = str(t.fetchone())
            if (t == 'None'): returnedString += '"' + str(row) + '": "Not Enrolled", '
            else: returnedString += '"' + str(row) + '": "Enrolled", '
        returnedString = returnedString[:-2] + "}"
        return returnedString
    if (request.method == 'GETNAME'):
        return session['name']
    if (request.method == 'CHANGEGRADE'):
        # Takes in username and password from the log-in page and assigns them to addedU and addedP
        changed = request.data
        changed = changed.decode()
        changed = json.loads(changed)
        changedID = changed['ID']
        changedClassID = changed['classID']
        changedGrade = changed['grade']
        print("Grade: " + str(changedGrade))

        junction_connection = junction_engine.connect()

        s = "DELETE FROM junction WHERE student='" + str(changedID) + "' AND class='" + str(changedClassID) + "'"
        result = junction_connection.execute(s)

        s = "INSERT INTO junction (student, class, grade) VALUES ('" + str(changedID) + "', '" + str(changedClassID) + "', '" + str(changedGrade) + "')"
        result = junction_connection.execute(s)
        junction_connection.close()
        return "success"

# This is where requests for data for a specific student is handled, you can only 'GET' from here
@app.route('/userdata/<calledusername>', methods = ['GET'])
def studPull(calledusername):
    if (request.method == 'GET'):
        print("current user: " + session['username'])
        print("attempted user: " + calledusername)
        # If the accessed user is the one currently logged in, redirect to their page, else redirect to the log-in page
        if (session['username'] == calledusername):
            print("User: " + str(session['username']))
            return render_template('posts.html')
        else: return redirect("http://127.0.0.1:5000/")

"""

@app.route('/class/<classID>', methods = ['GET'])
def classPull(classID):
    if (request.method == 'GET'):
        if (session['permission'] > 0):
            # Initializes connection to the junction database
            junction_connection = junction_engine.connect()
            # Pulls what classes the student is in from junction using their student id, assigns returned list to result
            s = "SELECT * FROM junction WHERE class='" + str(classID) + "'"
            result = junction_connection.execute(s)

            # Creates string returnedjson to store classes student is in along with their grade
            returnedjson = '{'
            # Iterates through returned list using parameter row for each line
            for row in result:
                # Converts the row of data to a string
                string = str(row)
                print(string)
                # Cuts out unnecessary portions of the data
                string = string[string.index(',')+2:]
                # Appends important part of data to returnedjson
                returnedjson += '"' + string[:string.index(',')] + '": "'
                string = string[string.index(',')+1:]
                string = string[string.index(',')+2:]
                returnedjson += string[:-1] + '", '
            #Cleans up returnedjson
            returnedjson = returnedjson[:-2] + "}"
            print(returnedjson)
            # Closes connection to the junction database
            junction_connection.close() 

            # Converts returnedjson into a python dictionary
            returnedjson = json.loads(returnedjson)
            # Connects to classes database
            students_connection = students_engine.connect()

            # Creates string finaljson to store all information of the classes the student is in
            finaljson = '{'

            # Iterates through returnedjson, such that key is the class id for each class the student is in
            for key in returnedjson:
                if (int(key) != int(session['id'])):
                    # Pulls class data for the key/current class
                    s = "SELECT name FROM students WHERE id='" + key + "'"
                    result = students_connection.execute(s)
                    # Appends class data to finaljson
                    finaljson += '"' + str(result.fetchone())[2:-3] + '": "'  + returnedjson[key] + '": "' + key + '", '
            # Cleans up finaljson
            finaljson = finaljson[:-2] + "}"

            # Closes connection to classes database
            students_connection.close()
            print(finaljson)

            # Return class information
            return finaljson
        return "fail"

"""


# Start the app
if __name__ == '__main__':
    app.run()