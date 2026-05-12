/**
 * Authentication Manager
 * Handles user authentication, token management, and role-based access
 * @module auth
 */

import CONFIG from './config.js';

let currentUser = null;
let fetchPromise = null;

export async function getCurrentUser() {
  if (currentUser) {
    return currentUser;
  }

  if (fetchPromise) {
    return fetchPromise;
  }

  const token = sessionStorage.getItem("access_token");
  if (!token) {
    return null;
  }

  fetchPromise = (async () => {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/user/me`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        });

        if (response.ok) {
        currentUser = await response.json();
        return currentUser;
      }

      sessionStorage.removeItem("access_token");
      return null;
    } catch (error) {
      console.error("Error fetching current user:", error);
      return null;
  } finally {
    fetchPromise = null;
  }
  })();

  return fetchPromise;
}

export const authUsers = { 
    isAuthenticated: () => !!currentUser,
    isGuest: () => !currentUser,
    isAdmin: () => currentUser?.role === CONFIG.ROLES.ADMIN,
    isAuthor: () => currentUser?.role === CONFIG.ROLES.AUTHOR,
    isUser: () => currentUser?.role === CONFIG.ROLES.USER,
};


export function getToken() {
    return sessionStorage.getItem("access_token");
}

export function setToken(token) { 
    return sessionStorage.setItem("access_token", token);
}

export function logout() {
    sessionStorage.removeItem("access_token");
    currentUser = null;
    window.location.href = "/";
}