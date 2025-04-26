// SmartHRM Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Sidebar toggle for mobile
    document.getElementById('sidebarToggle')?.addEventListener('click', function() {
        document.getElementById('sidebarMenu')?.classList.toggle('show');
    });

    // Notifications WebSocket
    setupNotificationsWebSocket();
});

// WebSocket for real-time notifications
function setupNotificationsWebSocket() {
    if (window.location.protocol === 'https:') {
        var wsProtocol = 'wss://';
    } else {
        var wsProtocol = 'ws://';
    }

    const notificationSocket = new WebSocket(
        wsProtocol + window.location.host + '/ws/notifications/'
    );

    notificationSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        
        // Update unread count
        if (data.hasOwnProperty('unread_count')) {
            updateUnreadCount(data.unread_count);
        }
        
        // Display new notification
        if (data.hasOwnProperty('message')) {
            showNotification(data.message);
        }
    };

    notificationSocket.onclose = function(e) {
        console.error('Notification socket closed unexpectedly');
        // Try to reconnect after 5 seconds
        setTimeout(function() {
            setupNotificationsWebSocket();
        }, 5000);
    };

    // Mark notification as read
    document.querySelectorAll('.notification-item').forEach(function(item) {
        item.addEventListener('click', function() {
            const notificationId = this.getAttribute('data-notification-id');
            if (notificationId) {
                notificationSocket.send(JSON.stringify({
                    'type': 'mark_as_read',
                    'notification_id': notificationId
                }));
            }
        });
    });

    // Mark all as read button
    document.getElementById('markAllAsRead')?.addEventListener('click', function() {
        notificationSocket.send(JSON.stringify({
            'type': 'mark_all_as_read'
        }));
    });
}

// Update notification badge count
function updateUnreadCount(count) {
    const badge = document.getElementById('notificationBadge');
    if (badge) {
        if (count > 0) {
            badge.textContent = count;
            badge.classList.remove('d-none');
        } else {
            badge.classList.add('d-none');
        }
    }
}

// Show notification toast
function showNotification(notification) {
    // Create toast element
    const toastContainer = document.getElementById('toastContainer');
    if (!toastContainer) return;
    
    const toast = document.createElement('div');
    toast.className = 'toast';
    toast.setAttribute('role', 'alert');
    toast.setAttribute('aria-live', 'assertive');
    toast.setAttribute('aria-atomic', 'true');
    
    // Set priority class
    let bgClass = 'bg-primary';
    if (notification.priority === 'high') {
        bgClass = 'bg-warning';
    } else if (notification.priority === 'urgent') {
        bgClass = 'bg-danger';
    }
    
    // Create toast content
    toast.innerHTML = `
        <div class="toast-header ${bgClass} text-white">
            <strong class="me-auto">${notification.title}</strong>
            <small>${timeAgo(new Date(notification.created_at))}</small>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="toast" aria-label="Close"></button>
        </div>
        <div class="toast-body">
            ${notification.message}
            ${notification.requires_action && notification.action_url ? 
                `<div class="mt-2 pt-2 border-top">
                    <a href="${notification.action_url}" class="btn btn-sm btn-primary">${notification.action_text || 'Xem chi tiết'}</a>
                </div>` : ''}
        </div>
    `;
    
    // Add to container
    toastContainer.appendChild(toast);
    
    // Initialize and show toast
    const bsToast = new bootstrap.Toast(toast, {
        autohide: true,
        delay: 5000
    });
    bsToast.show();
    
    // Remove from DOM after hidden
    toast.addEventListener('hidden.bs.toast', function() {
        toast.remove();
    });
}

// Format time ago
function timeAgo(date) {
    const seconds = Math.floor((new Date() - date) / 1000);
    
    let interval = seconds / 31536000;
    if (interval > 1) {
        return Math.floor(interval) + " năm trước";
    }
    
    interval = seconds / 2592000;
    if (interval > 1) {
        return Math.floor(interval) + " tháng trước";
    }
    
    interval = seconds / 86400;
    if (interval > 1) {
        return Math.floor(interval) + " ngày trước";
    }
    
    interval = seconds / 3600;
    if (interval > 1) {
        return Math.floor(interval) + " giờ trước";
    }
    
    interval = seconds / 60;
    if (interval > 1) {
        return Math.floor(interval) + " phút trước";
    }
    
    return "Vừa xong";
}
