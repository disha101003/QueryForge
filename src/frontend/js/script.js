document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signupForm');
    const loginForm = document.getElementById('loginForm');
    const messageDiv = document.getElementById('message');
    const searchBox = document.getElementById('searchBox'); // Assuming you have a search box in your HTML

    function displayMessage(message, isError = false) {
        messageDiv.textContent = message;
        messageDiv.style.color = isError ? 'red' : 'green';
    }

    // Search function
    function search() {
        if (searchBox) {
            alert('Search for: ' + searchBox.value);
        }
    }

    // Add event listener for search action
    if (searchBox) {
        searchBox.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault(); // Prevent form submission if part of a form
                search();
            }
        });
    }

    if (signupForm) {
        signupForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const username = this.username.value.trim();
            const email = this.email.value.trim();
            const password = this.password.value;

            if (username.length < 3) {
                displayMessage('Username must be at least 3 characters long', true);
                return;
            }

            if (password.length < 6) {
                displayMessage('Password must be at least 6 characters long', true);
                return;
            }

            // If validation passes, submit the form
            this.submit();
        });
    }

    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = this.email.value.trim();
            const password = this.password.value;

            if (!email || !password) {
                displayMessage('Please enter both email and password', true);
                return;
            }

            // If validation passes, submit the form
            this.submit();
        });
    }
});
