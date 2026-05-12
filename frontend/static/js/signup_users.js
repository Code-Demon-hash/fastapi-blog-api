import { CONFIG } from '/static/js/config.js';
import { getErrorMessage, showModal } from './utils';

const registerForm = document.getElementById('registerForm');
const passwordInput = document.getElementById('password');
const confirmPasswordInput = document.getElementById('confirmPassword');
const passwordError = document.getElementById('passwordError');

confirmPasswordInput.addEventListener('input', () => {
    if (passwordInput.value !== confirmPasswordInput.value) {
        passwordError.classList.remove('d-none');
        confirmPasswordInput.setCustomvalidity('Passwords do not match');
    } else {
        passwordError.classList.add('d-none');
        confirmPasswordInput.setCustomvalidity('');
    }
});

registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    if (passwordInput.value !== confirmPasswordInput.value) {
        passwordError.classList.remove('d-none');
        return;
    }

    const formData = new FormData(registerForm);
    const selectRole = formData.get('role');

    const userData = {
    username: formData.get('username'),
    password: formData.get('password'),
    };

    let endpoint = "";
    if (selectRole === CONFIG.ROLES.ADMIN) {
        endpoint = `${CONFIG.API_BASE_URL}/admin/`;
    } else if (selectRole === CONFIG.ROLES.AUTHOR) {
        endpoint = `${CONFIG.API_BASE_URL}/author/signup`;
    } else {
        endpoint = `${CONFIG.API_BASE_URL}/user/create_account`;
    }

    try {
        const response = await fetch(endpoint, { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(userData),
    });

    if (response.ok) {
        document.getElementById('successMessage').textContent =
        'Account created successfully! Please login.';
        showModal('successModal');
        window.location.href = '/login';
        return;
    } else {
        const error = await response.json();
        document.getElementById('errorMessage').textContent = getErrorMessage(error);
        showModal('errorModal');
    }
    } catch (error) {
        document.getElementById('errorMessage').textContent =
        'Network error. Please check your connection and try again.';
        showModal('errorModal');
        return;
    }
});
   