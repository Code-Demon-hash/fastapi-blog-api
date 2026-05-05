/**
 * Authentication Manager
 * Handles user authentication, token management, and role-based access
 * @module auth
 */

import CONFIG from './config.js';

export class AuthenticatonManager {
    constructor() {
        this.token = this.getToken();
        this.user = this.getUser();
        this.role = this.getRole();
    }

    setToken(token) {
        this.token = token;
        sessionStorage.setItem(CONFIG.TOKEN_KEY, token);
    }

    getToken() {
        return sessionStorage.getItem(CONFIG.TOKEN_KEY);
    }

    clearToken() {
        this.token = null;
        sessionStorage.removeItem(CONFIG.TOKEN_KEY);
    }

    setUser(user) {
        this.user = user;
        sessionStorage.setItem(CONFIG.USER_KEY, JSON.stringify(user));
    }

    getUser() {
        try {
            const user = sessionStorage.getItem(CONFIG.USER_KEY);
            if (!user) return null;
            return JSON.parse(user);
        } catch (error) {
            return null;
        }
    }

    setRole(role) {
        this.role = role;
        sessionStorage.setItem(CONFIG.ROLE_KEY, role);
    }

    getRole() {
        return sessionStorage.getItem(CONFIG.ROLE_KEY) || CONFIG.ROLES.GUEST;
    }

    isAuthenticated() {
        return !!this.getToken();
    }

    isGuest() {
        return !this.isAuthenticated();
    }

    isUser() {
        return this.getRole() === CONFIG.ROLES.USER;
    }

    isAuthor() {
        return this.getRole() === CONFIG.ROLES.AUTHOR || this.isAdmin();
    }

    isAdmin() {
        return this.getRole() === CONFIG.ROLES.ADMIN;
    }

    hasRole(role) {
        const userRole = this.getRole();
        if (role === CONFIG.ROLES.ADMIN) {
            return userRole === CONFIG.ROLES.ADMIN;
        }
        if (role === CONFIG.ROLES.AUTHOR) {
            return userRole === CONFIG.ROLES.AUTHOR || userRole === CONFIG.ROLES.ADMIN;
        }
        return userRole === role;
    }

    logout() {
        this.clearToken();
        sessionStorage.removeItem(CONFIG.USER_KEY);
        sessionStorage.removeItem(CONFIG.ROLE_KEY);
        this.user = null;
        this.role = CONFIG.ROLES.GUEST;
    }

    requireAuth() {
        if (!this.isAuthenticated()) {
            throw new Error("Please log in to access this resource.");
        }
    }

    requireRole(role) {
        if (!this.hasRole(role)) {
            throw new Error("You do not have permission to access this resource.");
        }
    }
}

export const authManager = new AuthenticatonManager();
export default authManager;