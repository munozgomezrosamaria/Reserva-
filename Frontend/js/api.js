/**
 * API Client for Reserval Backend
 * Handles all communication with the Django REST API
 */

const API_BASE_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:8000/api' 
    : 'https://reserva-kuiz.onrender.com/api';

class ApiClient {
    constructor() {
        this.baseUrl = API_BASE_URL;
    }

    // --- Token Management ---

    getAccessToken() {
        return localStorage.getItem('access_token');
    }

    getRefreshToken() {
        return localStorage.getItem('refresh_token');
    }

    saveTokens(access, refresh) {
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
    }

    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_data');
    }

    saveUserData(user) {
        localStorage.setItem('user_data', JSON.stringify(user));
    }

    getUserData() {
        const data = localStorage.getItem('user_data');
        return data ? JSON.parse(data) : null;
    }

    isAuthenticated() {
        return !!this.getAccessToken();
    }

    // --- HTTP Helpers ---

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers,
        };

        const token = this.getAccessToken();
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        try {
            let response = await fetch(url, { ...options, headers });

            // If 401, try refreshing the token
            if (response.status === 401 && this.getRefreshToken()) {
                const refreshed = await this.refreshToken();
                if (refreshed) {
                    headers['Authorization'] = `Bearer ${this.getAccessToken()}`;
                    response = await fetch(url, { ...options, headers });
                } else {
                    this.logout();
                    return null;
                }
            }

            return response;
        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    }

    async refreshToken() {
        try {
            const response = await fetch(`${this.baseUrl}/token/refresh/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ refresh: this.getRefreshToken() }),
            });

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('access_token', data.access);
                return true;
            }
            return false;
        } catch {
            return false;
        }
    }

    // --- Auth ---

    async login(email, password) {
        try {
            const response = await fetch(`${this.baseUrl}/token/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                const data = await response.json();
                this.saveTokens(data.access, data.refresh);
                // Fetch user profile
                await this.fetchProfile();
                return { success: true };
            }
            return { success: false, error: 'Correo o contraseña incorrectos' };
        } catch (err) {
            console.error(err);
            return { success: false, error: 'Error de conexión con el servidor. Intenta de nuevo.' };
        }
    }

    async register(firstName, email, password1, password2) {
        try {
            const response = await fetch(`${this.baseUrl}/users/register/`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    first_name: firstName,
                    email,
                    password1,
                    password2,
                }),
            });

            const data = await response.json();

            if (response.ok) {
                this.saveTokens(data.tokens.access, data.tokens.refresh);
                this.saveUserData(data.user);
                return { success: true };
            }

            return { success: false, errors: data };
        } catch (err) {
            console.error(err);
            alert('Error de red: No se pudo conectar con el servidor.');
            return { success: false, errors: {} };
        }
    }

    async fetchProfile() {
        const response = await this.request('/users/profile/');
        if (response && response.ok) {
            const user = await response.json();
            this.saveUserData(user);
            return user;
        }
        return null;
    }

    logout() {
        this.clearTokens();
        window.location.href = '/';
    }

    // --- Services ---

    async getServices() {
        const response = await this.request('/services/');
        if (response && response.ok) {
            return await response.json();
        }
        return [];
    }

    // --- Reservations ---

    async getReservations() {
        const response = await this.request('/reservations/');
        if (response && response.ok) {
            return await response.json();
        }
        return [];
    }

    async createReservation(date, numberPersons, serviceId) {
        const response = await this.request('/reservations/', {
            method: 'POST',
            body: JSON.stringify({
                date,
                number_persons: numberPersons,
                service: serviceId,
            }),
        });

        if (response && response.ok) {
            return { success: true, data: await response.json() };
        }

        let errorMessage = 'Error al crear la reserva';
        if (response) {
            try {
                const data = await response.json();
                // DRF returns errors in different formats, try to find a message
                errorMessage = data.detail || data.message || Object.values(data)[0] || errorMessage;
            } catch (e) {
                console.error('Error parsing response:', e);
            }
        }

        return { success: false, error: errorMessage };
    }
}

// Global instance
const api = new ApiClient();
