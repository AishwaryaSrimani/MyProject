function deleteBtn() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    
    // Validate username and password
    if (!username || !password) {
        alert('Please enter both username and password');
        return;
    }
    
    // Send a DELETE request to the server
    fetch('/delete_acc', {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => {
        if (response.ok) {
            response.text().then(data => {
                alert(data); // Display error message
            });  // Redirect to the register page
        } else {
            alert('Account deleted successfully');
            // Redirect the user to another page or perform other actions as needed
            window.location.href = '/register';
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to delete account'); // Display error message
    });
}