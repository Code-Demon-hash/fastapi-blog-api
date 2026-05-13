import { showModal, getErrorMessage, updateUIByRole } from '/static/js/utils.js';
import { getToken, authUsers, getCurrentUser } from './auth';
import { CONFIG } from '/static/js/config.js';

updateUIByRole();

const createBlogForm = document.getElementById('createBlogForm');
const myBlogs = document.getElementById('my-blogs');
const dashBoardStats = document.getElementById('dashboard-stats');

async function initAuthor() { 
    try {
        const user = await getCurrentUser();
        if (!user || (!authUsers.isAuthor() && authUsers.isAdmin())) {
            throw new Error("You do not have permission to access this resource.");
        }
        loadAuthorDashboard(user);
    }catch (error) {
        document.getElementById('errorMessage').textContent =
    'Access denied';
    showModal('errorModal');
} 
}

async function loadAuthorDashboard(user) { 
        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/blog/`,{
                headers: {
                    'Authorization': `Bearer ${getToken()}`
                }
            });

            if (!response.ok) throw new Error('Failed to load blogs.');

            const allBlogs = await response.json();

            const userBlogs = authUsers.isAdmin()
            ? allBlogs
            : allBlogs.filter(blog => blog.author ?.username === user.username);

            const totalPosts = userBlogs.length;
            const publishedPosts = userBlogs.filter(blog => blog.status === CONFIG.BLOG_STATUS.PUBLISHED).length;
            const totalLikes = userBlogs.reduce((sum, blog) => sum + (blog.likes || 0), 0);

            dashBoardStats.innerHTML = `
                <div class="col-md-4 mb-3">
                    <div class="card bg-light shadow-sm text-center p-3">
                        <h6 class="text-muted">Total Posts</h6>
                        <h3 class="fw-bold">${totalPosts}</h3>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card bg-light shadow-sm text-center p-3">
                        <h6 class="text-success">Published</h6>
                        <h3 class="fw-bold text-success">${publishedPosts}</h3>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card bg-light shadow-sm text-center p-3">
                        <h6 class="text-primary">Total Likes</h6>
                        <h3 class="fw-bold text-primary">${totalLikes}</h3>
                    </div>
                </div>
            `;

            if (userBlogs.length > 0) {
                myBlogs.innerHTML = userBlogs.map(blog => `
                    <div class="col-12 mb-2">
                        <div class="card p-3 shadow-sm d-flex flex-row justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-0">${blog.title}</h6>
                                <small class="badge ${blog.status === 'published' ? 'bg-success' : 'bg-warning'}">${blog.status}</small>
                            </div>
                            <span class="text-muted small"><i class="fas fa-heart text-danger"></i> ${blog.likes || 0}</span>
                        </div>
                    </div>
                `).join('');

                document.querySelectorAll('.delete-blog-btn').forEach(btn => {
                    btn.addEventListener('click', () => deleteblog(btn.dataset.id));
                });
            } else {
                myBlogs.innerHTML = '<div class="col-12 text-center text-muted"><p>No blogs yet. Start writing!</p></div>';
            }

        } catch (error) {
            dashBoardStats.innerHTML = `<div class="alert alert-danger">${error.message}</div>`;
        }
    } 

    if (dashBoardStats || myBlogs) {
        loadDashboard();
    }
        
    if (createBlogForm) {
        createBlogForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const submitBtn = createBlogForm.querySelector('button[type="submit"]');
            if(submitBtn) submitBtn.disabled = true;

            const formData = new FormData(createBlogForm);
                const blogData = {
                title: formData.get('title'),
                content: formData.get('content'),
                status: CONFIG.BLOG_STATUS.PENDING
            };

            try {
                const response = await fetch(`${CONFIG.API_BASE_URL}/blog/create`, {
                    method: 'POST', 
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${getToken()}`
                    },
                    body: JSON.stringify(blogData)
                });

                if (response.ok) {
                    document.getElementById('successMessage').textContent = 
                    "Blog submitted for review.";
                    showModal('StatusModal');

                    window.location.href = '/dashboard';
                } else {
                    const error = await response.json();
                    document.getElementById('errorMessage').textContent = getErrorMessage(error);
                    showModal('StatusModal');
                }
            } catch (error) {
                document.getElementById('errorMessage').textContent =
                'Network error. Please check your connection and try again.';
                showModal('StatusModal');
            } finally {
                if (submitBtn) {
                    submitBtn.disabled = false;
                }
            }
        });
    }

    async function deleteblog(blogId) {

        if (!authUsers.isAdmin() && !authUsers.isAuthor()) {
            document.getElementById('errorMessage').textContent = "You do not have right to perform this action.";
            showModal('successModal');
            return;
        }
        if (!confirm("Are you sure you want to permanently delete this blog post?")) return;

        try {
            const response = await fetch(`${CONFIG.API_BASE_URL}/blog/delete/${blogId}`, { 
                method: 'DELETE',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${getToken()}`
                }
            });

            if (response.ok) {
                document.getElementById('successMessage').textContent = 
                'Blog post successfully deleted';
                showModal('successModal');

                const user = await getCurrentUser();
                loadAuthorDashboard(user);
            } else {
                const error = await response.json();
                document.getElementById('errorMessage').textContent = getErrorMessage(error);
                showModal('errorModal');
            }
        }  catch (error) {
            document.getElementById('errorMessage').textContent = 
            'Network error. Please check your connection and try again.';
            showModal('successModal');
        }
    }

    if (dashBoardStats || myBlogs || createBlogForm) {
        initAuthor();
    }