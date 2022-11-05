var name = "null"
var password = "null"


async function readLogin() {
    username = document.getElementById("username").value;
    password = document.getElementById("password").value;
    //password = stringToHash(password);

    const response = await fetch('http://127.0.0.1:5000/student', {
            method: 'PASS', 
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({username, password})})
            const data = await response.text();
            document.getElementById("gradebook").innerHTML = data;
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