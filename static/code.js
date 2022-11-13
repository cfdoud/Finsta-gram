//Logging in/Session Management

function hash(str) {
    let seed = 69420727;
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

async function readLogin() {
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    password = hash(password);
    

    const response = await fetch('http://127.0.0.1:5000/student', {
        method: 'PASS', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({username, password})});
    
    const data = await response.text();
    document.getElementById("gradebook").innerHTML = data;

    if (data.charAt(0) == 'S') location.href = "student/" + username;
}

async function logOut() {
    const response = await fetch('http://127.0.0.1:5000/student', {method: 'LOGOUT'});
    location.href = "http://127.0.0.1:5000/";
}


// Table Fillers

async function fillTable() {
    const response = await fetch('http://127.0.0.1:5000/student', { method: 'CLASSES',});
    var data = await response.text();

    data = data.substring(data.indexOf("'") + 1);
    var table = document.getElementById("myTable");
    while(true) {
        var newRow = table.insertRow(table.length);
        var cell1 = newRow.insertCell(table.length);
        var cell2 = newRow.insertCell(table.length);
        var cell3 = newRow.insertCell(table.length);
        var cell4 = newRow.insertCell(table.length);

        cell1.innerHTML = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf("'")+1);
        data = data.substring(data.indexOf("'")+1);
        cell2.innerHTML = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf("'")+1);
        data = data.substring(data.indexOf("'")+1);
        cell3.innerHTML = data.substring(0, data.indexOf("'"));
        data = data.substring(data.indexOf('"')+1);
        data = data.substring(data.indexOf('"')+1);
        cell4.innerHTML = data.substring(0, data.indexOf('"')) + '%';
        data = data.substring(data.indexOf('"')+1);

        
        if (data.indexOf("'") == -1) break;
        data = data.substring(data.indexOf("'") + 1);
    }
}






























async function addStudent() {
        name = document.getElementById("student-name").value;
        grade = document.getElementById("student-grade").value;

        const response = await fetch('http://127.0.0.1:5000/data', {
            method: 'POST', 
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({name, grade})})
            const data = await response.text();
            document.getElementById("gradebook").innerHTML = data;
}

async function editStudent() {
    name = document.getElementById("student-name").value;
    grade = Number(document.getElementById("student-grade").value);
    name.replaceAll(' ', '%20');

    const response = await fetch('http://127.0.0.1:5000/data/' + name, {
        method: 'PUT', 
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({"grade": grade})})
        const data = await response.text();
        document.getElementById("gradebook").innerHTML = data;
        search();
}

async function deleteStudent() {
    name = document.getElementById("student-name").value;
    name.replaceAll(' ', '%20');

    const response = await fetch('http://127.0.0.1:5000/data/' + name, {method: 'DELETE',})
        const data = await response.text();
        document.getElementById("gradebook").innerHTML = data;
}

async function getStudents() {
    const response = await fetch('http://127.0.0.1:5000/data', {method: 'GET', });
    const data = await response.text();
    document.getElementById("gradebook").innerHTML = data;
}

async function search() {
    student = document.getElementById("student-name").value;
    student.replaceAll(' ', '%20');
    const response = await fetch('http://127.0.0.1:5000/data/' + student, {method: 'GET', });
    const data = await response.text();
    document.getElementById("listedStudent").innerHTML = data;
}