import { config } from "./config.js";
import { isAuthenticated, removeLocalStorage, getCurrentAdmin } from "../actions/authentication.js";

let currentUser = null;
let token = null;
let allUsers = [];
let allPending = [];
let currentRoleFilter = 'all';


async function initializeDashboard() {
    const user = isAuthenticated();

    if (!user) {
        redirectToLogin();
        return;
    }

    token = user.access_token || user.token;

    const admin = await getCurrentAdmin(token);

    if (!admin) {
        redirectToLogin();
        return;
    }

    currentUser = admin;
    showDashboard();
}

function redirecToLogin() {
    window.location.href = "/login.html";
}
initializeDashboard();


function showDashboard() {
    document.getElementById('guardLoading').style.display = 'none';
    document.getElementById('app').style.display = 'flex';

    renderIcons();
    initSidebar();
    initNav();
    initRoleFilter();
    loadAll();
}

function initSidebar() {
    const { username } = currentUser;

    const sidebarName = document.getElementById("sidebarName");
    const sidebarAvatar = document.getElementById("sidebarAvatar");
    const welcomeName = document.getElementById("welcomeName");
    const logoutButton = document.getElementById("logoutBtn");

    sidebarName.textContent = username;
    sidebarAvatar.textContent = username.slice(0, 2).toUpperCase;
    welcomeName.textContent = username;

    logoutButton.addEventListener('click', () => {
    removeLocalStorage('user');
    window.location.href = '/login.html';
  });
}

function initNav() {
  const navLinks = document.querySelectorAll('.nav-item');
  const views = document.querySelectorAll('.view');

  function showView(viewName) {
    pageViews.forEach(view => {
        const isCurrentView = view.id === `view-${viewName}`;
        view.classList.toggle('active', isCurrentView);
    });

    navigationItems.forEach(item => {
        const isCurrentLink = item.dataset.view === viewName;
        item.classList.toggle('item', isCurrentLink);
    });
  }

   navigationItems.forEach(item => {
        item.addEventListener('click', (event) => {
            event.preventDefault();

            const selectedView = item.dataset.view;
            showView(selectedView);
        });
    });

    document.querySelectorAll('[data-goto]').forEach(button => {
        button.addEventListener('click', (event) => {
            event.preventDefault();

            const destination = button.dataset.goto;
            showView(destination);
        });
    });
}

async function apiFetch(path, options = {}) {
  const res = await fetch(`${CONFIG.API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
  });

  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.detail || `Request failed: ${res.status}`);
  }

  const text = await res.text();
  return text ? JSON.parse(text) : null;
}

async function loadAll() {
    try {
        await Promise.all([
            loadUsers(),
            loadPending(),
        ]);

        renderDashboardStats();

    } catch (error) {
        console.error('Failed to load dashboard data.', error);
    }
}

async function loadUsers() {
    const tableBody = document.getElementById('userTableBody');

    try {
        allUsers = await apiFetch('/admin/users');

        renderUserTable();

    } catch (error) {
        console.error('Failed to load users.', error);

        tableBody.innerHTML = `
            <tr>
                <td colspan="4">
                    <div class="empty-state">
                        Unable to load users. Please refresh the page and try again.
                    </div>
                </td>
            </tr>
        `;
    }
}

async function loadPending() {
    const recentPending = document.getElementById('recentPendingList');
    const pendingTable = document.getElementById('allPendingList');

    try {
        allPending = await apiFetch('/blog/pending');

        renderRecentPending();

        renderAllPending();

    } catch (error) {
        console.error('Failed to load pending posts.', error);

        const emptyState = `
            <div class="empty-state">
                Unable to load pending posts. Please refresh the page and try again.
            </div>
        `;

        recentPending.innerHTML = emptyState;
        pendingTable.innerHTML = emptyState;
    }
}

function renderDashboardStats() {
    const totalUsersCard = document.getElementById('statTotalUsers');
    const pendingPostsCard = document.getElementById('statPendingPosts');
    const adminsCard = document.getElementById('statAdmins');
    const regularUsersCard = document.getElementById('statRegularUsers');

    const adminUsers = allUsers.filter(user => {
        return user.role === config.ROLES.ADMIN;
    });

    const regularUsers = allUsers.filter(user => {
        return user.role === config.ROLES.USER;
    });

    totalUsersCard.textContent = allUsers.length;
    pendingPostsCard.textContent = allPending.length;
    adminsCard.textContent = adminUsers.length;
    regularUsersCard.textContent = regularUsers.length;
}

function renderRecentPending() {
    const recentPendingList = document.getElementById('recentPendingList');

    if (allPending.length === 0) {
        recentPendingList.innerHTML = `
            <div class="empty-state">
                Nothing is waiting for review right now.
            </div>
        `;
        return;
    }

    const recentPosts = allPending.slice(0, 5);

    recentPendingList.innerHTML = recentPosts
        .map(post => pendingRowHTML(post))
        .join('');

    renderIcons(recentPendingList);
    attachPendingActions(recentPendingList);
}

function renderAllPending() {
    const pendingList = document.getElementById('allPendingList');

    if (allPending.length === 0) {
        pendingList.innerHTML = `
            <div class="empty-state">
                Nothing is waiting for review right now.
            </div>
        `;
        return;
    }

    pendingList.innerHTML = allPending
        .map(post => pendingRowHTML(post))
        .join('');

    renderIcons(pendingList);
    attachPendingActions(pendingList);
}

function pendingRowHTML(post) {
    const authorName = post.author?.username ?? 'Unknown author';

    return `
        <div class="pending-row" data-id="${post.id}">
            <div class="pending-row__info">
                <div class="pending-row__title">
                    ${escapeHtml(post.title)}
                </div>

                <div class="pending-row__meta">
                    by ${escapeHtml(authorName)}
                </div>
            </div>

            <div class="pending-row__actions">
                <button
                    class="btn-success"
                    data-action="approve"
                    data-id="${post.id}"
                >
                    <i data-icon="check"></i>
                    Publish
                </button>

                <button
                    class="btn-danger"
                    data-action="reject"
                    data-id="${post.id}"
                >
                    <i data-icon="x"></i>
                    Reject
                </button>
            </div>
        </div>
    `;
}

function attachPendingActions(container) {
    const approveButtons = container.querySelectorAll('[data-action="approve"]');
    const rejectButtons = container.querySelectorAll('[data-action="reject"]');

    approveButtons.forEach(button => {
        button.addEventListener('click', () => {
            const postId = Number(button.dataset.id);
            approvePost(postId);
        });
    });

    rejectButtons.forEach(button => {
        button.addEventListener('click', () => {
            const postId = Number(button.dataset.id);
            rejectPost(postId);
        });
    });
}

async function approvePost(postId) {
    const shouldPublish = confirm(
        'Publish this post? Once published, it will be visible to all readers.'
    );

    if (!shouldPublish) {
        return;
    }

    try {
        await apiFetch(`/blog/${postId}/submit`, {
            method: 'PUT',
        });

        await loadPending();

        renderDashboardStats();

    } catch (error) {
        alert(error.message || 'Unable to publish this post. Please try again.');
    }
}

async function rejectPost(postId) {
    const shouldReject = confirm(
        'Reject this post? It will be permanently deleted, and the author will need to submit it again.'
    );

    if (!shouldReject) {
        return;
    }

    try {
        await apiFetch(`/blog/delete/${postId}`, {
            method: 'DELETE',
        });

        await loadAll();

    } catch (error) {
        console.error('Failed to reject post.', error);
        alert(error.message || 'Unable to reject this post. Please try again.');
    }
}

function initRoleFilter() {
    const filterChips = document.querySelectorAll('#roleFilterRow .filter-chip');

    filterChips.forEach(chip => {
        chip.addEventListener('click', () => {

            filterChips.forEach(filter => {
                filter.classList.remove('active');
            });

            chip.classList.add('active');

            currentRoleFilter = chip.dataset.filter;

            renderUserTable();
        });
    });
}

function renderUserTable() {
    const tableBody = document.getElementById('userTableBody');

    const usersToDisplay =
        currentRoleFilter === 'all'
            ? allUsers
            : allUsers.filter(user => user.role === currentRoleFilter);

    if (usersToDisplay.length === 0) {
        tableBody.innerHTML = `
            <tr>
                <td colspan="4">
                    <div class="empty-state">
                        No users found for this role.
                    </div>
                </td>
            </tr>
        `;
        return;
    }

    tableBody.innerHTML = usersToDisplay
        .map(user => userRowHTML(user))
        .join('');

    renderIcons(tableBody);
    attachUserActions(tableBody);
}

function userRowHTML(user) {
    const isCurrentAdmin = user.id === currentAdmin.id;

    const initials = (user.username || '?')
        .slice(0, 2)
        .toUpperCase();

    const email = user.email ?? '';

    return `
        <tr data-id="${user.id}">
            <td>
                <div class="user-cell">

                    <div class="user-cell__avatar">
                        ${initials}
                    </div>

                    <div>
                        <div class="user-cell__name">
                            ${escapeHtml(user.username)}

                            ${isCurrentAdmin
                                ? '<span class="you-badge">You</span>'
                                : ''
                            }
                        </div>

                        <div class="user-cell__email">
                            ${escapeHtml(email)}
                        </div>
                    </div>

                </div>
            </td>

            <td>
                <span class="role-badge role-badge--${user.role}">
                    ${user.role}
                </span>
            </td>

            <td class="text-dim">
                ${formatDate(user.created_at)}
            </td>

            <td class="text-right">
                ${
                    isCurrentAdmin
                        ? ''
                        : `
                            <button
                                class="btn-danger btn-sm"
                                data-action="delete-user"
                                data-id="${user.id}"
                            >
                                <i data-icon="trash"></i>
                                Delete
                            </button>
                        `
                }
            </td>
        </tr>
    `;
}

function attachUserActions(tableBody) {
    const deleteButtons = tableBody.querySelectorAll(
        '[data-action="delete-user"]'
    );

    deleteButtons.forEach(button => {
        button.addEventListener('click', () => {
            const userId = Number(button.dataset.id);
            deleteUser(userId);
        });
    });
}

async function deleteUser(userId) {
    const selectedUser = allUsers.find(user => user.id === userId);

    if (!selectedUser) {
        return;
    }

    const shouldDelete = confirm(
        `Delete ${selectedUser.username}'s account permanently? This action cannot be undone.`
    );

    if (!shouldDelete) {
        return;
    }

    try {
        await apiFetch(`/admin/users/${userId}`, {
            method: 'DELETE',
        });

        await loadAll();

    } catch (error) {
        console.error('Failed to delete user.', error);

        alert(
            error.message ||
            'Unable to delete this user. Please try again.'
        );
    }
}

function formatDate(dateString) {
    if (!dateString) {
        return '—';
    }

    const date = new Date(dateString);

    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
    });
}

function escapeHtml(text) {
    const element = document.createElement('div');

    element.textContent = text ?? '';

    return element.innerHTML;
}
