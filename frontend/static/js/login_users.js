import { CONFIG } from '/static/js/config.js';
import { updateUIByRole, getErrorMessage, showModal } from '/static/js/utils.js';

const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(loginForm);

    const endpoints = [
        `${CONFIG.API_BASE_URL}/admin/login`,
        `${CONFIG.API_BASE_URL}/author/login`,
        `${CONFIG.API_BASE_URL}/user/token`
    ];

    for (const url of endpoints) {
        try {
        const response = await fetch(url, { 
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            sessionStorage.setItem('access_token', data.access_token);

            updateUIByRole();
            document.getElementById('successMessage').textContent =
            'Login successful!';
            showModal('successModal');

            window.location.href = '/';
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
    }
});