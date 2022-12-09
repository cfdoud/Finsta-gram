// Hashing function, used to obfuscate passwords so they cannot be easily retreived from the database
function hash(str) {
    // Custom seed/"Salt" for hash function
    let seed = 69420727;

    // I'm gonna be honest idk what the rest of this function is I stole it off stack overflow
    let h1 = 0xdeadbeef ^ seed, h2 = 0x41c6ce57 ^ seed;
    for (let i = 0, ch; i < str.length; i++) {
        ch = str.charCodeAt(i);
        h1 = Math.imul(h1 ^ ch, 2654435761);
        h2 = Math.imul(h2 ^ ch, 1597334677);
    }
        
    h1 = Math.imul(h1 ^ (h1 >>> 16), 2246822507) ^ Math.imul(h2 ^ (h2 >>> 13), 3266489909);
    h2 = Math.imul(h2 ^ (h2 >>> 16), 2246822507) ^ Math.imul(h1 ^ (h1 >>> 13), 3266489909);
        
    return 4294967296 * (2097151 & h2) + (h1 >>> 0);
}

// Login function, called when you press Log In
async function readLogin() {
    // Reads username and password and assigns them to a value
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    // Hashes password
    password = hash(password);
    
    // Calls the PASS function in /student as seen in index.py, assigns reply to variable data
    const response = await fetch('http://127.0.0.1:5000/userdata', {
        method: 'PASS', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password})});
    const data = await response.text();

    // Sets message on the login page to display result of log-in attempt
    document.getElementById("message").innerHTML = data;

    

    // If the log-in was successful, the message will begin with 'S' and you will be redirected to the page for your user (rest seen in /student/username in index.py)
    if (data.charAt(0) == 'S') {
        studentName = data.substring(data.indexOf("Hello")+1, data.indexOf("!")) 
        location.href = "userdata/" + username;
    }
}

// Log out function, called when you press Log Out
async function logOut() {
    // Calls LOGOUT function in /student as seen in index.py, redirects to log-in page
    const response = await fetch('http://127.0.0.1:5000/student', {method: 'LOGOUT'});
    location.href = "http://127.0.0.1:5000/";
}

async function initialize(table) {
    fillTableCurrClasses(table);
    getName();
}

// Table Fillers

// This function is automatically called in pages where it is relevant, it fills a matching table ("myTable") with the class information for the current user
async function fillTableCurrClasses(elementID) {
    // Calls CLASSES function in /student as seen in index.py, resultant information is saved in data
    const response = await fetch('http://127.0.0.1:5000/student', { method: 'CLASSES',});
    var data = await response.text();

    const response2 = await fetch('http://127.0.0.1:5000/student', { method: 'GETPERM',});
    var perm = await response2.text();
    perm = parseInt(perm)

    // Creates variable table connected to "myTable" in the html
    var table = document.getElementById(elementID);

    table.innerHTML = "";

    var newRow = table.insertRow(table.length);
    var cell1 = newRow.insertCell(table.length);
    var cell2 = newRow.insertCell(table.length);
    var cell3 = newRow.insertCell(table.length);
    var cell4 = newRow.insertCell(table.length);

    cell1.innerHTML = "Course";
    cell2.innerHTML = "Professor";
    cell3.innerHTML = "Time";
    cell4.innerHTML = "Students Enrolled";

    // Cuts data to begin at the start of the relevant information
    data = data.substring(data.indexOf("(") + 1);
    // Loops through each class until the information is emptied
    while(true) {
        // Creates a new row with the cells necessary, appending them to the current table
        var newRow = table.insertRow(table.length);
        var cell1 = newRow.insertCell(table.length);
        var cell2 = newRow.insertCell(table.length);
        var cell3 = newRow.insertCell(table.length);
        var cell4 = newRow.insertCell(table.length);

        var courseID = data.substring(0, data.indexOf(","));
        data = data.substring(data.indexOf("'")+1);
        var courseName = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf(",")+2);
        var studCount = data.substring(0, data.indexOf(","));
        data = data.substring(data.indexOf(",")+2);
        var studCapacity = data.substring(0, data.indexOf(","));
        data = data.substring(data.indexOf("'")+1);
        var time = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf(",")+3);
        var professor = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf(":") + 3);
        var grade = data.substring(0, data.indexOf('"')) + "%";

        if (perm == 0) cell1.innerHTML = courseName;
        else {
            cell1.innerHTML = '<button onclick="viewClass(' + courseID + ')">' + courseName + '</button>';
        }
        cell2.innerHTML = professor;
        cell3.innerHTML = time;
        cell4.innerHTML = studCount + "/" + studCapacity;


        if (data.indexOf("(") == -1) break;
        // Tab to next relevant information
        data = data.substring(data.indexOf("(") + 1);
    }
    document.getElementById("tablelabel").innerHTML = "Your Classes";
}

async function viewClass(classID) {
    const response = await fetch('http://127.0.0.1:5000/class/' + classID, { method: 'GET',});
    var data = await response.text();

    if (data == "fail") return;

    var table = document.getElementById("myTable");

    table.innerHTML = "";

    var newRow = table.insertRow(table.length);
    var cell1 = newRow.insertCell(table.length);
    var cell2 = newRow.insertCell(table.length);
    var cell3 = newRow.insertCell(table.length);

    cell1.innerHTML = "Student";
    cell2.innerHTML = "Grade";
    cell3.innerHTML = "New Grade";

    // Cuts data to begin at the start of the relevant information
    data = data.substring(data.indexOf('"') + 1);
    // Loops through each class until the information is emptied
    while(true) {
        // Creates a new row with the cells necessary, appending them to the current table
        var newRow = table.insertRow(table.length);
        var cell1 = newRow.insertCell(table.length);
        var cell2 = newRow.insertCell(table.length);
        var cell3 = newRow.insertCell(table.length);
        var cell4 = newRow.insertCell(table.length);

        var name = data.substring(0, data.indexOf('"'));
        data = data.substring(data.indexOf('"')+1);
        data = data.substring(data.indexOf('"')+1);
        var grade = data.substring(0, data.indexOf('"')) + "%";
        data = data.substring(data.indexOf('"')+1);
        data = data.substring(data.indexOf('"')+1);
        var ID = data.substring(0, data.indexOf('"'));
        data = data.substring(data.indexOf('"')+1);

        cell1.innerHTML = name;
        cell2.innerHTML = grade;
        cell3.innerHTML = '<input id="' + ID + '" type="text"/>';
        cell4.innerHTML = '<button onclick="changeGrade(' + ID + ', ' + classID + ')">Confirm</button>';


        if (data.indexOf('"') == -1) break;
        // Tab to next relevant information
        data = data.substring(data.indexOf('"') + 1);
    }
    document.getElementById("tablelabel").innerHTML = "Student Grades";
}

async function changeGrade(ID, classID) {
    var grade = parseInt(document.getElementById(ID).value);
    const response = await fetch('http://127.0.0.1:5000/student', {
        method: 'CHANGEGRADE', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ID, classID, grade})});
    const data = await response.text();

    viewClass(classID);
}

async function fillTableAllClasses(elementID) {
    const response = await fetch('http://127.0.0.1:5000/student', { method: 'ALLCLASSES',});
    var data = await response.text();

    var table = document.getElementById(elementID);

    table.innerHTML = "";

    var newRow = table.insertRow(table.length);
    var cell1 = newRow.insertCell(table.length);
    var cell2 = newRow.insertCell(table.length);
    var cell3 = newRow.insertCell(table.length);
    var cell4 = newRow.insertCell(table.length);
    var cell5 = newRow.insertCell(table.length);

    cell1.innerHTML = "Course";
    cell2.innerHTML = "Professor";
    cell3.innerHTML = "Time";
    cell4.innerHTML = "Students Enrolled";
    cell5.innerHTML = "Enrollment Status";

    // Cuts data to begin at the start of the relevant information
    data = data.substring(data.indexOf("(") + 1);
    // Loops through each class until the information is emptied
    while(true) {
        // Creates a new row with the cells necessary, appending them to the current table
        var newRow = table.insertRow(table.length);
        var cell1 = newRow.insertCell(table.length);
        var cell2 = newRow.insertCell(table.length);
        var cell3 = newRow.insertCell(table.length);
        var cell4 = newRow.insertCell(table.length);
        var cell5 = newRow.insertCell(table.length);

        var courseID = data.substring(0, data.indexOf(","));
        data = data.substring(data.indexOf("'")+1);
        var courseName = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf(",")+2);
        var studCount = data.substring(0, data.indexOf(","));
        data = data.substring(data.indexOf(",")+2);
        var studCapacity = data.substring(0, data.indexOf(","));
        data = data.substring(data.indexOf("'")+1);
        var time = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf(",")+3);
        var professor = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf(":") + 3);
        var inClass = data.substring(0, data.indexOf('"'));

        
        cell1.innerHTML = courseName;
        cell2.innerHTML = professor;
        cell3.innerHTML = time;
        cell4.innerHTML = studCount + "/" + studCapacity; 
        if (inClass == "Enrolled") cell5.innerHTML = '<button onclick="dropClass(-1, ' + courseID + ', ' + "'myTable'" + ')">Drop</button>';
        else cell5.innerHTML = '<button onclick="addClass(-1, ' + courseID + ', 0, ' + "'myTable'" + ')">Add</button>';


        if (data.indexOf("(") == -1) break;
        // Tab to next relevant information
        data = data.substring(data.indexOf("(") + 1);
    }
    document.getElementById("tablelabel").innerHTML = "All Classes";
}

async function addClass(studentID, classID, grade, elementID) {
    const response = await fetch('http://127.0.0.1:5000/student', {
        method: 'ADD', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({studentID, classID, grade})});
    const data = await response.text();

    fillTableAllClasses(elementID);
}

async function dropClass(studentID, classID, elementID) {
    const response = await fetch('http://127.0.0.1:5000/student', {
        method: 'DROP', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({studentID, classID})});
    const data = await response.text();

    fillTableAllClasses(elementID);
}

async function getName() {
    const response = await fetch('http://127.0.0.1:5000/student', { method: 'GETNAME',});
    var data = await response.text();
    console.log(data)
    document.getElementById("name").innerHTML = data;
    return data;
}