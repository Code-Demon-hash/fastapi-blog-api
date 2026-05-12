import { CONFIG } from 'static/js/config.js';
import { getToken, authUsers, getCurrentUser } from './auth';
import { showModal, getErrorMessage, updateUIByRole } from '/static/js/utils.js';

updateUIByRole(); 

const pendingBlogs = document.getElementById('pending-blogs');

async function initAdmin() {
    const user = await getCurrentUser();

    if (!user || !authUsers.isAdmin()) { 
        throw new Error("You do not have permission to access this resource.");
    }

    loadAdminDashboard();
}

async function loadAdminDashboard() {
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/blog/`, {
            headers: {
                'Authorization': `Bearer ${getToken()}`
            }
        });
        
        if (!response.ok) throw new Error('Failed to load blogs.');
        
        const allBlogs = await response.json();

        const pending = allBlogs.filter(blog => blog.status === CONFIG.BLOG_STATUS.PENDING);

        if (pending.length > 0) {
            pendingBlogs.innerHTML = pending.map(blog => `
            <div class="card mb-3 shadow-sm">
                        <div class="card-body">
                            <h5 class="card-title">${blog.title}</h5>
                            <p class="card-text text-muted">Author: ${blog.author?.username || 'Unknown'}</p>
                            <div class="mt-3">
                                <button class="btn btn-success btn-sm approve-btn" data-id="${blog.id}">
                                    Approve & Publish
                                </button>
                                <button class="btn btn-outline-danger btn-sm delete-btn" data-id="${blog.id}">
                                    Reject
                                </button>
                            </div>
                        </div>
                    </div>
                `).join('');
        } else {
            pendingBlogs.innerHTML = '<p class="text-center">No pending blogs.</p>';
        }
    } catch (error) {
        pendingBlogs.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
    }
}

    const approveBlog = async (blogId) => {
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/blog/${blogId}/submit`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getToken()}`
                },
                body: JSON.stringify({ status: CONFIG.BLOG_STATUS.PUBLISHED })
            });

            if (response.ok) {
                document.getElementById('successMessage').textContent = 
                "Blog has been published!";
                showModal('successModal');
                loadAdminDashboard();
            } else {
                const error = await response.json();
                document.getElementById('errorMessage').textContent = getErrorMessage(error);
                showModal('errorModal');
            }
        } catch (error) {
            document.getElementById('errorMessage').textContent = 
            'Network error. Please check your connection and try again.';
            showModal('successModal');
        }
    };

    if (pendingSection) {
        loadAdminDashboard();
    }

    approveBlog();
    initAdmin();