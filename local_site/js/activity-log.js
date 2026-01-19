// Activity Log functionality - shared across all pages
// Version 2.0 - Jan 2026 - Database-backed for persistent, shared logs
class ActivityLogger {
  constructor(pageName) {
    this.pageName = pageName;
    this.activityLog = [];
    // Use the same API base URL logic as api.js
    this.apiBaseUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
      ? 'http://localhost:8000'
      : 'https://bucksport-api.onrender.com';
  }

  async logActivity(action, details, itemId = null) {
    // Get user from auth manager if available
    let userName = 'Admin';
    if (typeof authManager !== 'undefined' && authManager.getCurrentUser()) {
      const user = authManager.getCurrentUser();
      userName = `${user.first_name} ${user.last_name}`;
    }
    
    const entry = {
      action: action,
      details: details,
      user: userName,
      page: this.pageName,
      item_id: itemId
    };
    
    try {
      // Save to database via API
      const response = await fetch(`${this.apiBaseUrl}/api/activity-logs`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(entry)
      });
      
      if (!response.ok) {
        console.error('Failed to log activity to database');
        // Fallback to localStorage if API fails
        this.fallbackToLocalStorage(entry);
      }
    } catch (error) {
      console.error('Error logging activity:', error);
      // Fallback to localStorage if API fails
      this.fallbackToLocalStorage(entry);
    }
  }
  
  fallbackToLocalStorage(entry) {
    const storageKey = `${this.pageName}_activity_log`;
    const logs = JSON.parse(localStorage.getItem(storageKey) || '[]');
    logs.unshift({...entry, timestamp: new Date().toISOString()});
    if (logs.length > 100) {
      logs.splice(100);
    }
    localStorage.setItem(storageKey, JSON.stringify(logs));
  }

  // Helper method to log changes with before/after values
  logChanges(itemName, originalData, newData, fieldsToCompare) {
    const changes = [];
    
    fieldsToCompare.forEach(field => {
      const oldValue = originalData[field] || 'N/A';
      const newValue = newData[field] || 'N/A';
      
      if (oldValue !== newValue) {
        const fieldLabel = field.charAt(0).toUpperCase() + field.slice(1);
        changes.push(`${fieldLabel}: "${oldValue}" → "${newValue}"`);
      }
    });
    
    if (changes.length > 0) {
      this.logActivity(`${itemName} Updated`, changes.join(', '));
    }
  }

  async fetchActivityLogs(pageFilter = null) {
    try {
      const url = pageFilter 
        ? `${this.apiBaseUrl}/api/activity-logs?page=${pageFilter}`
        : `${this.apiBaseUrl}/api/activity-logs`;
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Failed to fetch activity logs');
      }
      
      this.activityLog = await response.json();
      return this.activityLog;
    } catch (error) {
      console.error('Error fetching activity logs:', error);
      // Fallback to localStorage
      const storageKey = pageFilter ? `${pageFilter}_activity_log` : 'master_activity_log';
      this.activityLog = JSON.parse(localStorage.getItem(storageKey) || '[]');
      return this.activityLog;
    }
  }

  static async exportMasterLog() {
    try {
      const apiBaseUrl = window.API_BASE_URL || '';
      const response = await fetch(`${apiBaseUrl}/api/activity-logs`);
      const logs = await response.json();
      
      const dataStr = JSON.stringify(logs, null, 2);
      const dataBlob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(dataBlob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `activity_log_${new Date().toISOString().split('T')[0]}.json`;
      link.click();
      URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Error exporting activity log:', error);
      alert('Failed to export activity log');
    }
  }

  async renderActivityLog(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Show loading state
    container.innerHTML = '<p class="text-gray-500 text-center py-8">Loading activity logs...</p>';

    // Fetch logs from database
    await this.fetchActivityLogs(this.pageName);

    if (this.activityLog.length === 0) {
      container.innerHTML = '<p class="text-gray-500 text-center py-8">No activity recorded yet.</p>';
      return;
    }

    container.innerHTML = this.activityLog.map(entry => {
      const date = new Date(entry.timestamp);
      const timeStr = date.toLocaleString();
      return `
        <div class="border-b border-gray-200 py-3 px-4 hover:bg-gray-50">
          <div class="flex justify-between items-start">
            <div class="flex-1">
              <p class="font-semibold text-purple-900">${entry.action}</p>
              <p class="text-sm text-gray-600">${entry.details}</p>
              <p class="text-xs text-gray-500 mt-1">By: ${entry.user}</p>
            </div>
            <div class="text-xs text-gray-500 ml-4 whitespace-nowrap">${timeStr}</div>
          </div>
        </div>
      `;
    }).join('');
  }

  initializeModal() {
    const modal = document.getElementById('activityLogModal');
    const openBtn = document.getElementById('viewActivityLog');
    const closeBtn = document.getElementById('closeActivityLog');

    console.log('initializeModal called', {
      modal: !!modal,
      openBtn: !!openBtn,
      closeBtn: !!closeBtn
    });

    if (openBtn) {
      console.log('Adding click handler to activity log button');
      openBtn.addEventListener('click', async () => {
        console.log('Activity log button clicked!');
        if (!modal) {
          console.error('Modal element not found!');
          return;
        }
        await this.renderActivityLog('activityLogContent');
        modal.classList.remove('hidden');
      });
    } else {
      console.error('Activity log button (viewActivityLog) not found!');
    }

    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        modal.classList.add('hidden');
      });
    }

    // Close modal when clicking outside the content
    if (modal) {
      modal.addEventListener('click', (e) => {
        if (e.target === modal) {
          modal.classList.add('hidden');
        }
      });
    } else {
      console.error('Activity log modal element not found!');
    }
  }
}

// Create modal HTML (call this function to inject the modal into the page)
function createActivityLogModal() {
  const modalHTML = `
    <!-- Activity Log Modal -->
    <div id="activityLogModal" class="hidden fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white rounded-lg w-full max-w-4xl max-h-[90vh] overflow-hidden mx-4">
        <div class="flex justify-between items-center border-b p-4 bg-purple-700 text-white">
          <h3 class="text-lg font-semibold"><i class="fas fa-history mr-2"></i>Activity Log</h3>
          <button id="closeActivityLog" class="text-white hover:text-gray-200 text-xl">
            <i class="fas fa-times"></i>
          </button>
        </div>
        <div id="activityLogContent" class="overflow-y-auto max-h-[calc(90vh-4rem)]">
          <!-- Activity entries will be inserted here -->
        </div>
      </div>
    </div>
  `;
  document.body.insertAdjacentHTML('beforeend', modalHTML);
}
