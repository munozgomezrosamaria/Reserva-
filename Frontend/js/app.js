/**
 * App.js - Main application logic
 * Handles navbar auth state, routing helpers, and shared behaviors
 */

document.addEventListener('DOMContentLoaded', () => {
    updateNavbar();
});

function updateNavbar() {
    const authLinks = document.getElementById('auth-links');
    if (!authLinks) return;

    if (api.isAuthenticated()) {
        const user = api.getUserData();
        const name = user ? user.first_name : 'Usuario';
        authLinks.innerHTML = `
            <li class="nav-item">
                <a class="nav-link" href="/pages/reservations.html">Mis Reservas</a>
            </li>
            <li class="nav-item">
                <span class="nav-link">${name}</span>
            </li>
            <li class="nav-item">
                <button class="btn btn-dark ms-3" onclick="api.logout()">Cerrar sesión</button>
            </li>
        `;
    } else {
        authLinks.innerHTML = `
            <li class="nav-item">
                <a class="btn btn-dark ms-3" href="/pages/login.html">Iniciar sesión</a>
            </li>
        `;
    }
}

function showAlert(message, type = 'success') {
    const container = document.getElementById('alert-container');
    if (!container) return;
    
    container.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show mt-3" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;

    setTimeout(() => {
        container.innerHTML = '';
    }, 5000);
}

function requireAuth() {
    if (!api.isAuthenticated()) {
        window.location.href = '/pages/login.html';
        return false;
    }
    return true;
}
