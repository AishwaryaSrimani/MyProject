function updatePassword() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const new_password = document.getElementById("new_password").value;

    fetch('/change_password', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            username: username,
            password: password,
            new_password: new_password
        })
    })
    .then(response => response.text())
    .then(data => {
        alert(data); // Display success or failure message
    })
    .catch(error => {
        console.error('Error:', error);
    });
}