/**
 * Authentication utility for Bucksport Little League
 * Handles user authentication, authorization, and session management
 */

class AuthManager {
  constructor() {
    this.token = localStorage.getItem('auth_token');
    this.userInfo = JSON.parse(localStorage.getItem('user_info') || 'null');
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!this.token && !!this.userInfo;
  }

  /**
   * Get current user information
   */
  getCurrentUser() {
    return this.userInfo;
  }

  /**
   * Check if current user is an admin
   */
  isAdmin() {
    return this.userInfo && this.userInfo.role === 'admin';
  }

  /**
   * Check if current user is a board member
   */
  isBoardMember() {
    return this.userInfo && this.userInfo.role === 'board_member';
  }

  /**
   * Get authorization header for API requests
   */
  getAuthHeader() {
    return {
      'Authorization': `Bearer ${this.token}`
    };
  }

  /**
   * Verify token with backend
   */
  async verifyToken() {
    if (!this.token) {
      return false;
    }

    try {
      const response = await fetch('/auth/me', {
        headers: this.getAuthHeader()
      });

      if (response.ok) {
        const userData = await response.json();
        this.userInfo = userData;
        localStorage.setItem('user_info', JSON.stringify(userData));
        return true;
      } else {
        this.logout();
        return false;
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      this.logout();
      return false;
    }
  }

  /**
   * Logout user
   */
  logout() {
    localStorage.removeItem('auth_token');
    localStorage.removeItem('user_info');
    this.token = null;
    this.userInfo = null;
    window.location.href = '/login.html';
  }

  /**
   * Require authentication - redirect to login if not authenticated
   */
  async requireAuth() {
    if (!this.isAuthenticated()) {
      window.location.href = '/login.html';
      return false;
    }

    // Verify token is still valid
    const isValid = await this.verifyToken();
    if (!isValid) {
      window.location.href = '/login.html';
      return false;
    }

    return true;
  }

  /**
   * Require admin role - show error if not admin
   */
  requireAdmin() {
    if (!this.isAdmin()) {
      alert('Admin access required for this action.');
      return false;
    }
    return true;
  }

  /**
   * Check if user has permission for a specific page
   */
  hasPagePermission(pageName) {
    // Admins have access to everything
    if (this.isAdmin()) {
      return { read: true, write: true };
    }

    // Board members have read-only access to fundraising
    if (this.isBoardMember()) {
      if (pageName === 'fundraising') {
        return { read: true, write: false };
      }
      // Full access to other pages
      return { read: true, write: true };
    }

    return { read: false, write: false };
  }

  /**
   * Initialize auth UI elements on page
   */
  initializeUI() {
    if (!this.userInfo) return;

    // Update user info in header if element exists
    const userInfoEl = document.getElementById('userInfo');
    if (userInfoEl) {
      userInfoEl.innerHTML = `
        <div class="flex items-center gap-3">
          <div class="text-right">
            <p class="font-semibold text-white">${this.userInfo.first_name} ${this.userInfo.last_name}</p>
            <p class="text-xs text-purple-200">${this.userInfo.role === 'admin' ? 'Administrator' : 'Board Member'}</p>
          </div>
          <button onclick="authManager.logout()" class="bg-red-600 hover:bg-red-700 text-white px-3 py-2 rounded-md text-sm font-semibold transition-colors">
            <i class="fas fa-sign-out-alt"></i> Logout
          </button>
        </div>
      `;
    }

    // Update activity logger user
    if (typeof activityLogger !== 'undefined') {
      activityLogger.user = `${this.userInfo.first_name} ${this.userInfo.last_name}`;
    }
  }

  /**
   * Apply page-specific permissions
   */
  applyPagePermissions(pageName) {
    const permissions = this.hasPagePermission(pageName);

    if (!permissions.write) {
      // Hide all edit/add/delete buttons
      const editButtons = document.querySelectorAll('[data-action="edit"], [data-action="add"], [data-action="delete"], .edit-btn, .delete-btn, .add-btn');
      editButtons.forEach(btn => {
        btn.style.display = 'none';
      });

      // Disable form submissions
      const forms = document.querySelectorAll('form');
      forms.forEach(form => {
        form.addEventListener('submit', (e) => {
          e.preventDefault();
          alert('You have read-only access to this page.');
        });
      });

      // Show read-only banner
      const header = document.querySelector('header');
      if (header) {
        const banner = document.createElement('div');
        banner.className = 'bg-yellow-100 border-l-4 border-yellow-500 text-yellow-700 p-4 mb-4';
        banner.innerHTML = `
          <div class="flex items-center">
            <i class="fas fa-lock mr-3 text-xl"></i>
            <div>
              <p class="font-bold">Read-Only Access</p>
              <p class="text-sm">You can view this page but cannot make changes.</p>
            </div>
          </div>
        `;
        header.after(banner);
      }
    }
  }
}

// Create global auth manager instance
const authManager = new AuthManager();

// Auto-protect pages (exclude login page)
if (!window.location.pathname.includes('login.html')) {
  document.addEventListener('DOMContentLoaded', async () => {
    const isAuthenticated = await authManager.requireAuth();
    if (isAuthenticated) {
      authManager.initializeUI();
      
      // Determine current page and apply permissions
      const pageName = window.location.pathname.split('/').pop().replace('.html', '') || 'index';
      if (pageName === 'fundraising') {
        authManager.applyPagePermissions('fundraising');
      }
    }
  });
}
