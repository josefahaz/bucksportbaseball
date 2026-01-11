/**
 * Mobile Detection and Redirect Script
 * Detects mobile devices and redirects to mobile-specific pages
 */

(function() {
  // Check if we're already on a mobile page
  const currentPath = window.location.pathname;
  const isOnMobilePage = currentPath.includes('/mobile/');
  
  // Check if user has manually chosen desktop version (stored in sessionStorage)
  const preferDesktop = sessionStorage.getItem('preferDesktop') === 'true';
  
  // Detect mobile device
  function isMobileDevice() {
    // Check screen width (768px is common tablet/mobile breakpoint)
    const isSmallScreen = window.innerWidth <= 768;
    
    // Check user agent for mobile devices
    const mobileUserAgent = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
    
    // Check for touch capability (most mobile devices)
    const hasTouch = 'ontouchstart' in window || navigator.maxTouchPoints > 0;
    
    // Consider it mobile if small screen OR mobile user agent
    return isSmallScreen || mobileUserAgent;
  }
  
  // Get the mobile version URL for current page
  function getMobileUrl() {
    const path = window.location.pathname;
    const filename = path.split('/').pop() || 'index.html';
    
    // Build mobile URL - go to mobile subfolder
    const basePath = path.substring(0, path.lastIndexOf('/') + 1);
    return basePath + 'mobile/' + filename + window.location.search + window.location.hash;
  }
  
  // Get the desktop version URL from mobile page
  function getDesktopUrl() {
    const path = window.location.pathname;
    // Remove 'mobile/' from the path
    const desktopPath = path.replace('/mobile/', '/');
    return desktopPath + window.location.search + window.location.hash;
  }
  
  // Redirect to mobile version if on desktop page and using mobile device
  function checkAndRedirect() {
    if (!isOnMobilePage && isMobileDevice() && !preferDesktop) {
      window.location.href = getMobileUrl();
    }
  }
  
  // Function to switch to desktop version (can be called from mobile pages)
  window.switchToDesktop = function() {
    sessionStorage.setItem('preferDesktop', 'true');
    window.location.href = getDesktopUrl();
  };
  
  // Function to switch to mobile version (can be called from desktop pages)
  window.switchToMobile = function() {
    sessionStorage.removeItem('preferDesktop');
    window.location.href = getMobileUrl();
  };
  
  // Function to clear preference and use auto-detection
  window.clearViewPreference = function() {
    sessionStorage.removeItem('preferDesktop');
  };
  
  // Run redirect check when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', checkAndRedirect);
  } else {
    checkAndRedirect();
  }
})();
