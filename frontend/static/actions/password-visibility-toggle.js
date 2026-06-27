export function initPasswordToggle() {
  const fields = [
    'password',
    'currentPassword',
    'newPassword',
    'confirmPassword',
    'confirmNewPassword',
  ];

  fields.forEach(id => {
    const passwordInput = document.getElementById(id);
    if (passwordInput) {
        createToggleButton(passwordInput);
    }
    });
}

function createToggleButton(inputField) {
    const toggleButton = document.createElement('span');
    toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
    toggleButton.classList.add('password-toggle');

    inputField.parentNode.insertBefore(toggleButton, inputField.nextSibling);

    toggleButton.addEventListener('click', function() {
        if (inputField.type === 'password') {
            inputField.type = 'text';
            toggleButton.innerHTML = '<i class="fas fa-eye-slash"></i>';
        } else {
            inputField.type = 'password';
            toggleButton.innerHTML = '<i class="fas fa-eye"></i>';
        }
    })
}