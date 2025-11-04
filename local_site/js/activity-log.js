// Activity Log functionality - shared across all pages
class ActivityLogger {
  constructor(pageName) {
    this.pageName = pageName;
    this.storageKey = `${pageName}_activity_log`;
    this.masterLogKey = 'master_activity_log';
    this.activityLog = JSON.parse(localStorage.getItem(this.storageKey) || '[]');
  }

  logActivity(action, details) {
    const entry = {
      timestamp: new Date().toISOString(),
      action: action,
      details: details,
      user: 'Admin', // TODO: Replace with actual user from authentication
      page: this.pageName
    };
    
    // Add to page-specific log (keep last 100)
    this.activityLog.unshift(entry);
    if (this.activityLog.length > 100) {
      this.activityLog = this.activityLog.slice(0, 100);
    }
    localStorage.setItem(this.storageKey, JSON.stringify(this.activityLog));
    
    // Add to master log (unlimited history)
    this.addToMasterLog(entry);
  }

  addToMasterLog(entry) {
    const masterLog = JSON.parse(localStorage.getItem(this.masterLogKey) || '[]');
    masterLog.unshift(entry);
    localStorage.setItem(this.masterLogKey, JSON.stringify(masterLog));
  }

  static getMasterLog() {
    return JSON.parse(localStorage.getItem('master_activity_log') || '[]');
  }

  static clearMasterLog() {
    localStorage.setItem('master_activity_log', '[]');
    console.log('Master activity log cleared');
  }

  static exportMasterLog() {
    const masterLog = ActivityLogger.getMasterLog();
    const dataStr = JSON.stringify(masterLog, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `activity_log_${new Date().toISOString().split('T')[0]}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  renderActivityLog(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

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

    if (openBtn) {
      openBtn.addEventListener('click', () => {
        this.renderActivityLog('activityLogContent');
        modal.classList.remove('hidden');
      });
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
