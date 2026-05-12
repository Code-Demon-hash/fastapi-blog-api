import { authUsers } from "./auth";

export function getErrorMessage(error) {
    if (typeof error.detail === "string") {
        return error.detail;
    } else if (Array.isArray(error.detail)) {
        return error.detail.map((err) => err.msg).join(". ");
    }
    return "An error has occured. Please try again.";
}

export function formatDate(datestring) {
    const date = new Date(datestring);
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "long",
        day: "2-digit",
    });
}

export function escapeHtml(text) {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
}

export function showModal(modalId) {
    const modal = bootstrap.Modal.getOrCreateInstance( 
        document.getElementById(modalId),
    );
    modal.show();
    return modal;
}

export function hideModal(modalId) {
    const modal = bootstrap.Modal.getInstance(document.getElementById(modalId));
    if (modal) modal.hide();
}

export function updateUIByRole() {
    const isGuest = authUsers.isGuest();
    const isUser = authUsers.isUser();
    const isAuthor = authUsers.isAuthor
    const isAdmin = authUsers.isAdmin();
    const isAuthenticated = authUsers.isAuthenticated();

    document.querySelectorAll('.guest-only').forEach(element => element.style.display = 'none');
    document.querySelectorAll('.authenticated').forEach(element => element.style.display = 'none');
    document.querySelectorAll('.author-only').forEach(element => element.style.display = 'none');
    document.querySelectorAll('.admin-only').forEach(element => element.style.display = 'none');

    if (isGuest) {
        document.querySelectorAll('.guest-only').forEach(element => element.style.display = '');
    }
    if (isAuthenticated) {
        document.querySelectorAll('.authenticated').forEach(element => element.style.display = '');
    }
    if (isAuthor) {
        document.querySelectorAll('.author-only').forEach(element => element.style.display = '');
    }
    if (isAdmin) {
        document.querySelectorAll('.admin-only').forEach(element => element.style.display = '');
    }
}