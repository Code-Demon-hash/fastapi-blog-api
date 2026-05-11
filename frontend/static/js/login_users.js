import { CONFIG } from '/static/js/config.js';
import { updateUIByRole, getErrorMessage } from '/static/js/utils.js';

const loginForm = document.getElementById('loginForm');

loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(loginForm);

    try {
        const response = await fetch(`${CONFIG.API_URL}/user/token`, {
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            sessionStorage.setItem('access_token', data.access_token);

            updateUIByRole();
            alert('Login successfully');

            window.location.href = '#home';
            return;
        } else {
            const error = await response.json();
            getErrorMessage(error);
        }
    } catch (error) {
        alert('Network error. Please check your connection and try agian.');
        return;
    }

    try {
        const response = await fetch(`${CONFIG.API_URL}/admin/login`, { 
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            sessionStorage.setItem('access_token', data.access_token);

            updateUIByRole();
            alert('Login successfully');

            window.location.href = '#home';
            return;
        } else {
            const error = await response.json();
            getErrorMessage(error);
        }
    } catch (error) {
        alert('Network error. Please check your connection and try agian.');
        return;
    }

    try {
        const response = await fetch(`${CONFIG.API_URL}/author/login`, { 
            method: 'POST',
            body: formData,
        });

        if (response.ok) {
            const data = await response.json();
            sessionStorage.setItem('access_token', data.access_token);

            updateUIByRole();
            alert('Login successfully');
            return;

            window.location.href = '#home';
        } else {
            const error = await response.json();
            getErrorMessage(error);
        }
    } catch (error) {
        alert('Network error. Please check your connection and try agian.');
        return;
    }
});