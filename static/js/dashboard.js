// Dashboard JavaScript
document.addEventListener('DOMContentLoaded', function() {
  // Sidebar Toggle
  const sidebarToggle = document.getElementById('sidebarToggle');
  const sidebar = document.getElementById('sidebar');
  const mainContent = document.querySelector('.main-content');
  
  if (sidebarToggle) {
    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('collapsed');
      mainContent.classList.toggle('expanded');
      
      // Save preference
      const isCollapsed = sidebar.classList.contains('collapsed');
      localStorage.setItem('sidebarCollapsed', isCollapsed);
    });
  }
  
  // Restore sidebar state
  const savedState = localStorage.getItem('sidebarCollapsed');
  if (savedState === 'true') {
    sidebar.classList.add('collapsed');
    mainContent.classList.add('expanded');
  }
  
  // Task Checkboxes
  const taskCheckboxes = document.querySelectorAll('.task-checkbox');
  taskCheckboxes.forEach(checkbox => {
    checkbox.addEventListener('change', function(e) {
      const taskItem = this.closest('.task-item');
      const taskId = taskItem?.dataset.taskId;
      
      if (taskId) {
        updateTaskStatus(taskId, this.checked);
      }
    });
  });
  
  // Mobile Menu
  const mobileMenuButton = document.getElementById('mobileMenuButton');
  if (mobileMenuButton) {
    mobileMenuButton.addEventListener('click', function() {
      sidebar.classList.toggle('mobile-open');
    });
  }
  
  // Close sidebar when clicking outside on mobile
  document.addEventListener('click', function(e) {
    if (window.innerWidth <= 768) {
      if (!sidebar.contains(e.target) && !mobileMenuButton?.contains(e.target)) {
        sidebar.classList.remove('mobile-open');
      }
    }
  });
});

// Update task status
async function updateTaskStatus(taskId, completed) {
  try {
    const response = await fetch(`/api/tasks/${taskId}/`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCookie('csrftoken')
      },
      body: JSON.stringify({
        status: completed ? 'done' : 'todo'
      })
    });
    
    if (!response.ok) {
      throw new Error('Failed to update task');
    }
    
    // Show success message
    showNotification('Task updated successfully', 'success');
  } catch (error) {
    console.error('Error updating task:', error);
    showNotification('Failed to update task', 'error');
    
    // Revert checkbox
    const checkbox = document.querySelector(`[data-task-id="${taskId}"] .task-checkbox`);
    if (checkbox) {
      checkbox.checked = !completed;
    }
  }
}

// Show notification
function showNotification(message, type = 'info') {
  const notification = document.createElement('div');
  notification.className = `alert alert-${type}`;
  notification.style.position = 'fixed';
  notification.style.top = '80px';
  notification.style.right = '20px';
  notification.style.zIndex = '9999';
  notification.style.minWidth = '300px';
  notification.textContent = message;
  
  document.body.appendChild(notification);
  
  setTimeout(() => {
    notification.remove();
  }, 3000);
}

// Get CSRF token
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

// Debounce function
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Handle window resize
window.addEventListener('resize', debounce(() => {
  const sidebar = document.getElementById('sidebar');
  if (window.innerWidth > 768) {
    sidebar?.classList.remove('mobile-open');
  }
}, 250));