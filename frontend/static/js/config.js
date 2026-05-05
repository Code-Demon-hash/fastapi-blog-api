export const CONFIG = {
    API_BASE_URL: 'http://localhost:8000/api',

    TOKEN_STORAGE_KEY: 'blog_access_token',
    USER_CACHE_KEY: 'blog_current_user',
    ROLE_CACHE_KEY: 'blog_user_roles',

    ROLES: {
        ADMIN: 'admin',
        AUTHOR: 'author',
        USER: 'user',
    }, 
    
    BLOG_STATUS: {
        PENDING: 'pending',
        PUBLISHED: 'published',
    },

    ENDPOINTS: {
        USER_SIGNUP: '/user/create_account',
        USER_LOGIN: '/user/token',
        USER_PRoFILE: '/users/me',

        AUTHOR_SIGNUP: '/author/signup',
        AUTHOR_LOGIN: '/author/login',

        ADMIN_SIGNUP: '/admin/',
        ADMIN_LOGIN: '/admin/login',

        BLOG_CREATE: '/blog/create',
        BLOG_LIST: '/blog/',
        BLOG_BY_ID: (id) => '/blog/${id}',
        BLOG_UPDATE: (blog_id) => '/blog/update/${blog_id}',
        BLOG_DELETE: (id) => '/blog/delete/${id}',
        BLOG_SUBMIT: (blog_id) => '/blog/${id}/submit',

        COMMENT_CREATE: (blog_id) => '/comment/create/${blog_id}',
        COMMENT_ON_BLOG: (blog_id) => '/comment/${blog_id}',

        LIKE_BLOG: (blog_id) => '/like/${blog_id}',
        UNLIKE_BLOG: (blog_id) => '/like/delete${blog_id}',
}
};

export default CONFIG;