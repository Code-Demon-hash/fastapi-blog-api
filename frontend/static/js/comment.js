import { CONFIG } from './config.js';
import { getErrorMessage, showModal, formatDate } from './utils.js';
import { authUsers, getCurrentUser } from './auth.js';

let activeBlogId = null;

export async function initializeComments(blogId) {
    activeBlogId = blogId;
    await loadComment();
}

async function loadComment() {
    const commentSection = document.getElementById('comments-section'); 
    if (!commentSection || !activeBlogId) return;

    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/comment/${activeBlogId}`);

        if (!response.ok) {
            throw new Error('Failed to fetch');
        }
        const data = await response.json();
        if (commentsContainer) {
            commentsContainer.innerHTML = data.map(comment => renderComment(comment, getCurrentUser)).join('');
        }
    } catch(error) {
        console.error('Error:', error);
        commentSection.innerHTML = '<p class="text-danger">Could not load comments.</p>';
    }
}

async function handleCommentCreate() { 
    const content = commentInput.value.trim();
    submitCommentBtn.disabled = true;
    submitCommentBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Adding...';

    const token = sessionStorage.getItem("access_token");
    try {
        const response = await fetch(`${CONFIG.API_BASE_URL}/comment/create/${activeBlogId}`, {
            method: 'POST', 
            headers: {
                'Authorization': `Bearer ${token}`, 
                'Content-Type': 'text/html'
            },
             body: JSON.stringify({
                content: content
            })
        });

        if (response.ok) {
            commentInput.value = '';
            await loadComment();
        } else {
            const error = await response.json();
            document.getElementById('errorMessage').textContent = getErrorMessage(error);
            showModal('errorModal');
        }
    } catch (error) {
        document.getElementById('errorMessage').textContent = 
        'Network error. Please check your connection and try again.';
        showModal('successModal');
    } finally {
            submitCommentBtn.disabled = false;
            submitCommentBtn.innerHTML = 'Send';
         }
}

function renderComment(comment, getCurrentUser) { 
        const isOwner = getCurrentUser && getCurrentUser.id === comment.user_id;
        const isAdmin = getCurrentUser && getCurrentUser.role === CONFIG.ROLES.ADMIN;
        const actions = (isOwner || isAdmin) ? `
            <div class="comment-actions mt-2">
                <button class="btn btn-sm btn-primary edit-comment-btn" data-comment-id="${comment.id}">
                    <i class="bi bi-pencil"></i> Edit
                </button>
                <button class="btn btn-sm btn-danger delete-comment-btn" data-comment-id="${comment.id}">
                    <i class="bi bi-trash"></i> Delete
                </button>
            </div>` : '';
        
        return `
            <div class="comment-wrapper" data-comment-id="${comment.id}">
                <div class="comment-header d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <strong class="comment-author">${comment.user.username}</strong>
                        <small class="text-muted ms-2">${formatDate(comment.created_at)}</small>
                    </div>
                </div>
                <p class="comment-content mb-2">${comment.content}</p>
                ${actions}
            </div>`;
    }

document.addEventListener('DOMContentLoaded', () => {
    const commentInput = document.getElementById('commentInput');
    const submitCommentBtn = document.getElementById('submitCommentBtn');

    if (submitCommentBtn) {
         submitCommentBtn.addEventListener('click', handleCommentCreate);
    }
    
    if (commentInput) {
         commentInput.addEventListener('keypress', (event) => {
             if (event.key === 'Enter' && !event.shiftKey) {
                event.preventDefault();
                handleCommentCreate(); // Fixed call loop target to your creation function
             }
    });
    }
});