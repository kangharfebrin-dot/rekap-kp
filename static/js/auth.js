document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const authAlert = document.getElementById('authAlert');

    function showAlert(msg, isError = true) {
        authAlert.textContent = msg;
        authAlert.className = `alert ${isError ? 'alert-error' : 'alert-success'}`;
        authAlert.classList.remove('hidden');
    }

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;

        loginBtn.disabled = true;
        loginBtn.textContent = 'Loading...';

        try {
            const res = await fetch('/api/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            
            if (data.success) {
                window.location.href = data.role === 'admin' ? '/admin' : '/dashboard';
            } else {
                showAlert(data.message);
            }
        } catch (err) {
            showAlert('Terjadi kesalahan jaringan.');
        } finally {
            loginBtn.disabled = false;
            loginBtn.textContent = 'Login';
        }
    });

    registerBtn.addEventListener('click', async () => {
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        if (!username || !password) {
            showAlert('Isi username dan password untuk mendaftar!');
            return;
        }

        registerBtn.disabled = true;
        registerBtn.textContent = 'Loading...';

        try {
            const res = await fetch('/api/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            const data = await res.json();
            
            showAlert(data.message, !data.success);
        } catch (err) {
            showAlert('Terjadi kesalahan jaringan.');
        } finally {
            registerBtn.disabled = false;
            registerBtn.textContent = 'Daftar Baru';
        }
    });
});
