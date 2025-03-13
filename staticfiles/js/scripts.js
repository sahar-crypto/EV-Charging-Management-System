// scripts.js

// Function to display error messages
function displayError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.innerText = message;

    const container = document.querySelector('.container');
    container.insertBefore(errorDiv, container.firstChild);

    // Remove the error message after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Example: Add event listeners for form validation
document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', (event) => {
            const password1 = form.querySelector('input[name="password1"]');
            const password2 = form.querySelector('input[name="password2"]');

            if (password1 && password2 && password1.value !== password2.value) {
                event.preventDefault();
                displayError('Passwords do not match.');
            }
        });
    });
});