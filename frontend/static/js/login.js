import { login, authenticate, isAuthenticated } from '../actions/authentication.js';
import { initPasswordToggle } from '../actions/password-visibility-toggle.js';


const usernameInput = document.getElementById('username');
const passwordInput = document.getElementById('password');
const loginForm = document.getElementById('loginForm');


initPasswordToggle();

const currentUser = isAuthenticated();
if (currentUser) {
    redirectByRole(currentUser.role);
}


loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(loginForm);
    const username = formData.get('username').trim();
    const password = formData.get('password').trim();
    const role = formData.get('role') || 'user';

    try {
        const data = await login({ username, password }, role);

        if (!data || data.detail || !data.access_token) {
            const msg = data?.detail || 'Incorrect username or password.';
            usernameInput.setCustomValidity(msg);
            passwordInput.setCustomValidity(msg);

            passwordInput.reportValidity();
            return;
        }

        setToken(data.access_token);
        const user = await getCurrentUser();
        authenticate(
            { user: { ...user, token: data.access_token } },
            () => {
                redirectByRole(user?.role);
            }
        );
    } catch (error) {
        const msg =
        getErrorMessage(error) || 'Network error. Please check your connection and try again.';
        usernameInput.setCustomValidity(msg);
        passwordInput.setCustomValidity(msg);

        passwordInput.reportValidity();
        console.error('Login error:', error);
    }
});

function redirectByRole(role) {
    const destinations = {
        admin: '/admin.html',
        author: '/author.html',
        user: '/index.html'
    };
    window.location.href = destinations[role] ?? '/index.html';
}