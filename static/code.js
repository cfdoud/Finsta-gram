//Logging in/Session Management
var username = 'null'
var password = 'null'
var studentName = 'null'

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
    const response = await fetch('http://127.0.0.1:5000/student', {
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
        location.href = "student/" + username;
    }
}

// Log out function, called when you press Log Out
async function logOut() {
    // Calls LOGOUT function in /student as seen in index.py, redirects to log-in page
    const response = await fetch('http://127.0.0.1:5000/student', {method: 'LOGOUT'});
    location.href = "http://127.0.0.1:5000/";
}

async function initialize() {
    fillTableCurrClasses();
    getName();
}

// Table Fillers

// This function is automatically called in pages where it is relevant, it fills a matching table ("myTable") with the class information for the current user
async function fillTableCurrClasses() {
    // Calls CLASSES function in /student as seen in index.py, resultant information is saved in data
    const response = await fetch('http://127.0.0.1:5000/student', { method: 'CLASSES',});
    var data = await response.text();

    // Creates variable table connected to "myTable" in the html
    var table = document.getElementById("myTable");

    table.innerHTML = "";

    var newRow = table.insertRow(table.length);
    var cell1 = newRow.insertCell(table.length);
    var cell2 = newRow.insertCell(table.length);
    var cell3 = newRow.insertCell(table.length);
    var cell4 = newRow.insertCell(table.length);

    cell1.innerHTML = "Course";
    cell2.innerHTML = "Time";
    cell3.innerHTML = "Professor";
    cell4.innerHTML = "Grade";

    // Cuts data to begin at the start of the relevant information
    data = data.substring(data.indexOf("'") + 1);
    // Loops through each class until the information is emptied
    while(true) {
        // Creates a new row with the cells necessary, appending them to the current table
        var newRow = table.insertRow(table.length);
        var cell1 = newRow.insertCell(table.length);
        var cell2 = newRow.insertCell(table.length);
        var cell3 = newRow.insertCell(table.length);
        var cell4 = newRow.insertCell(table.length);

        

        // Reads information in single quotes, assuming starting at relevant information, assigns to cell1
        cell1.innerHTML = data.substring(0, data.indexOf("'"));
        // Tabs to next relevant information
        data = data.substring(data.indexOf("'")+1);
        data = data.substring(data.indexOf("'")+1);
        // Reads information in nearest single quotes, assuming starting at relevant information, assigns to cell2
        cell2.innerHTML = data.substring(0, data.indexOf("'"));
        // Tabs to next relevant information
        data = data.substring(data.indexOf("'")+1);
        data = data.substring(data.indexOf("'")+1);
        // Reads information in nearest single quotes, assuming starting at relevant information, assigns to cell3
        cell3.innerHTML = data.substring(0, data.indexOf("'"));
        // Tabs to next relevant information
        data = data.substring(data.indexOf('"')+1);
        data = data.substring(data.indexOf('"')+1);
        // Reads information in nearest double quotes, assuming starting at relevant information, assigns to cell4
        cell4.innerHTML = data.substring(0, data.indexOf('"')) + '%';

        // If there is no more information, break the loop and finish
        if (data.indexOf("'") == -1) break;
        // Tab to next relevant information
        data = data.substring(data.indexOf("'") + 1);
    }
}

async function fillTableAllClasses() {
    const response = await fetch('http://127.0.0.1:5000/student', { method: 'ALLCLASSES',});
    var data = await response.text();

    document.getElementById("testLabel").innerHTML = data;
}

async function addClass(studentID, classID, grade) {
    const response = await fetch('http://127.0.0.1:5000/student', {
        method: 'ADD', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({studentID, classID, grade})});
    const data = await response.text();

    fillTableCurrClasses();
}

async function dropClass(studentID, classID) {
    const response = await fetch('http://127.0.0.1:5000/student', {
        method: 'DROP', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({studentID, classID})});
    const data = await response.text();

    fillTableCurrClasses();
}

async function getName() {
    console.log("Bruh");
    const response = await fetch('http://127.0.0.1:5000/student', { method: 'GETNAME',});
    var data = await response.text();
    console.log(data)
    document.getElementById("name").innerHTML = data;
    return data;
}