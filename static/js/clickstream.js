// Clickstream Tracking System
// This file handles all user interaction tracking for the learning website

// Generate unique session ID if not exists
if (!sessionStorage.getItem('session_id')) {
    sessionStorage.setItem('session_id', generateSessionId());
}

// Generate unique session ID
function generateSessionId() {
    return 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// Main tracking function
function trackEvent(eventType, elementId, elementType, additionalData = {}) {
    const eventData = {
        event_type: eventType,
        element_id: elementId,
        element_type: elementType,
        page_url: window.location.href,
        additional_data: additionalData
    };

    // Send to backend API
    fetch('/api/track_event', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(eventData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('Event tracked:', eventData);
    })
    .catch(error => {
        console.error('Error tracking event:', error);
        // Store failed events in localStorage for retry
        storeFailedEvent(eventData);
    });
}

// Store failed events for retry
function storeFailedEvent(eventData) {
    const failedEvents = JSON.parse(localStorage.getItem('failed_events') || '[]');
    failedEvents.push({
        ...eventData,
        timestamp: Date.now()
    });
    localStorage.setItem('failed_events', JSON.stringify(failedEvents));
}

// Retry failed events
function retryFailedEvents() {
    const failedEvents = JSON.parse(localStorage.getItem('failed_events') || '[]');
    if (failedEvents.length === 0) return;

    failedEvents.forEach((event, index) => {
        fetch('/api/track_event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(event)
        })
        .then(response => response.json())
        .then(data => {
            // Remove successful event from failed events
            failedEvents.splice(index, 1);
            localStorage.setItem('failed_events', JSON.stringify(failedEvents));
        })
        .catch(error => {
            console.error('Failed to retry event:', error);
        });
    });
}

// Track page views
function trackPageView() {
    const pageTitle = document.title;
    const pageUrl = window.location.href;
    
    trackEvent('page_view', pageTitle, 'page', {
        page_title: pageTitle,
        referrer: document.referrer
    });
}

// Track clicks on interactive elements with specific categorization
function trackClicks() {
    document.addEventListener('click', function(event) {
        const target = event.target;
        
        // Track button clicks
        if (target.tagName === 'BUTTON' || target.classList.contains('btn')) {
            let buttonType = 'general_button';
            let buttonContext = 'unknown';
            
            // Determine button context
            if (target.classList.contains('btn-primary')) buttonContext = 'primary_action';
            else if (target.classList.contains('btn-secondary')) buttonContext = 'secondary_action';
            else if (target.classList.contains('btn-success')) buttonContext = 'success_action';
            else if (target.classList.contains('btn-danger')) buttonContext = 'danger_action';
            else if (target.classList.contains('btn-large')) buttonContext = 'large_action';
            
            trackEvent('click', target.textContent.trim() || target.className, 'button', {
                button_text: target.textContent.trim(),
                button_class: target.className,
                button_type: buttonType,
                button_context: buttonContext,
                click_location: getClickLocation(target)
            });
        }
        
        // Track link clicks
        if (target.tagName === 'A') {
            let linkType = 'general_link';
            let linkContext = 'unknown';
            
            // Determine link context
            if (target.href.includes('/course/')) linkContext = 'course_navigation';
            else if (target.href.includes('/lesson/')) linkContext = 'lesson_navigation';
            else if (target.href.includes('/dashboard')) linkContext = 'dashboard_navigation';
            else if (target.href.includes('/admin/')) linkContext = 'admin_navigation';
            else if (target.href.includes('/login')) linkContext = 'auth_navigation';
            else if (target.href.includes('/register')) linkContext = 'auth_navigation';
            
            trackEvent('click', target.href, 'link', {
                link_text: target.textContent.trim(),
                link_href: target.href,
                link_type: linkType,
                link_context: linkContext,
                click_location: getClickLocation(target)
            });
        }
        
        // Track form submissions
        if (target.tagName === 'INPUT' && target.type === 'submit') {
            let formType = 'general_form';
            let formContext = 'unknown';
            
            // Determine form context
            if (target.form && target.form.action.includes('/login')) formContext = 'login_form';
            else if (target.form && target.form.action.includes('/register')) formContext = 'register_form';
            else if (target.form && target.form.action.includes('/admin/login')) formContext = 'admin_login_form';
            
            trackEvent('click', 'form_submit', 'form', {
                form_id: target.form ? target.form.id : 'unknown',
                input_type: target.type,
                form_type: formType,
                form_context: formContext,
                click_location: getClickLocation(target)
            });
        }
        
        // Track quiz-specific clicks
        if (target.type === 'radio' || target.type === 'checkbox') {
            let quizContext = 'general_quiz';
            if (target.closest('.quiz-question')) quizContext = 'quiz_answer_selection';
            
            trackEvent('click', target.value || target.name, 'quiz_input', {
                input_type: target.type,
                input_name: target.name,
                input_value: target.value,
                quiz_context: quizContext,
                question_text: getQuestionText(target),
                click_location: getClickLocation(target)
            });
        }
        
        // Track navigation menu clicks
        if (target.closest('.nav-menu') || target.closest('.nav-links')) {
            trackEvent('click', target.textContent.trim() || target.className, 'navigation_menu', {
                menu_item: target.textContent.trim(),
                menu_class: target.className,
                click_location: getClickLocation(target)
            });
        }
    });
}

// Helper function to get click location context
function getClickLocation(element) {
    const rect = element.getBoundingClientRect();
    return {
        x: rect.left + rect.width / 2,
        y: rect.top + rect.height / 2,
        page_x: window.pageXOffset + rect.left + rect.width / 2,
        page_y: window.pageYOffset + rect.top + rect.height / 2
    };
}

// Helper function to get question text for quiz elements
function getQuestionText(element) {
    const questionElement = element.closest('.quiz-question');
    if (questionElement) {
        const questionText = questionElement.querySelector('h4, p');
        return questionText ? questionText.textContent.trim() : 'Unknown question';
    }
    return 'Not a quiz question';
}

// Track form interactions
function trackFormInteractions() {
    document.addEventListener('input', function(event) {
        const target = event.target;
        
        if (target.tagName === 'INPUT' || target.tagName === 'TEXTAREA' || target.tagName === 'SELECT') {
            // Track focus events
            if (event.type === 'focus') {
                trackEvent('form_interaction', target.name || target.id || 'unknown_field', 'form_field', {
                    field_name: target.name,
                    field_type: target.type,
                    action: 'focus'
                });
            }
            
            // Track change events for select elements
            if (event.type === 'change' && target.tagName === 'SELECT') {
                trackEvent('form_interaction', target.name || target.id || 'unknown_field', 'form_field', {
                    field_name: target.name,
                    field_type: target.type,
                    action: 'change',
                    selected_value: target.value
                });
            }
        }
    });
}

// Scroll tracking removed - not counting scroll events

// Track time spent on page
function trackTimeOnPage() {
    let startTime = Date.now();
    let timeTrackingInterval;
    
    // Track every 60 seconds (less frequent)
    timeTrackingInterval = setInterval(function() {
        const timeSpent = Math.round((Date.now() - startTime) / 1000);
        
        if (timeSpent % 60 === 0 && timeSpent > 0) {
            trackEvent('time_on_page', `time_${timeSpent}s`, 'time', {
                time_spent_seconds: timeSpent,
                page_url: window.location.href
            });
        }
    }, 1000);
    
    // Track when leaving page
    window.addEventListener('beforeunload', function() {
        const totalTimeSpent = Math.round((Date.now() - startTime) / 1000);
        trackEvent('page_exit', 'page_exit', 'page', {
            time_spent_seconds: totalTimeSpent,
            page_url: window.location.href
        });
        
        // Clear interval
        clearInterval(timeTrackingInterval);
    });
}

// Track mouse movements (throttled) - only for significant movements
function trackMouseMovements() {
    let lastMoveTime = 0;
    let lastPosition = { x: 0, y: 0 };
    const throttleDelay = 5000; // Track every 5 seconds, only if moved significantly
    
    document.addEventListener('mousemove', function(event) {
        const currentTime = Date.now();
        const deltaX = Math.abs(event.clientX - lastPosition.x);
        const deltaY = Math.abs(event.clientY - lastPosition.y);
        
        // Only track if moved more than 100px and enough time has passed
        if (currentTime - lastMoveTime > throttleDelay && (deltaX > 100 || deltaY > 100)) {
            trackEvent('mouse_movement', 'mouse_move', 'mouse', {
                mouse_x: event.clientX,
                mouse_y: event.clientY,
                delta_x: deltaX,
                delta_y: deltaY,
                page_url: window.location.href
            });
            
            lastMoveTime = currentTime;
            lastPosition = { x: event.clientX, y: event.clientY };
        }
    });
}

// Track keyboard interactions
function trackKeyboardInteractions() {
    document.addEventListener('keydown', function(event) {
        // Track specific key combinations
        if (event.ctrlKey || event.metaKey) {
            let keyCombo = '';
            if (event.ctrlKey) keyCombo += 'Ctrl+';
            if (event.metaKey) keyCombo += 'Cmd+';
            keyCombo += event.key.toUpperCase();
            
            trackEvent('keyboard', keyCombo, 'keyboard', {
                key: event.key,
                ctrl_key: event.ctrlKey,
                meta_key: event.metaKey,
                shift_key: event.shiftKey,
                alt_key: event.altKey
            });
        }
    });
}

// Track window resize events
function trackWindowResize() {
    let resizeTimeout;
    
    window.addEventListener('resize', function() {
        clearTimeout(resizeTimeout);
        
        resizeTimeout = setTimeout(function() {
            trackEvent('window_resize', 'window_resize', 'window', {
                window_width: window.innerWidth,
                window_height: window.innerHeight,
                screen_width: screen.width,
                screen_height: screen.height
            });
        }, 250); // Debounce resize events
    });
}

// Track visibility changes (tab switching, minimizing)
function trackVisibilityChanges() {
    let hidden, visibilityChange;
    
    if (typeof document.hidden !== "undefined") {
        hidden = "hidden";
        visibilityChange = "visibilitychange";
    } else if (typeof document.msHidden !== "undefined") {
        hidden = "msHidden";
        visibilityChange = "msvisibilitychange";
    } else if (typeof document.webkitHidden !== "undefined") {
        hidden = "webkitHidden";
        visibilityChange = "webkitvisibilitychange";
    }
    
    document.addEventListener(visibilityChange, function() {
        if (document[hidden]) {
            trackEvent('visibility_change', 'page_hidden', 'visibility', {
                action: 'hidden',
                page_url: window.location.href
            });
        } else {
            trackEvent('visibility_change', 'page_visible', 'visibility', {
                action: 'visible',
                page_url: window.location.href
            });
        }
    });
}

// Initialize all tracking functions
function initializeTracking() {
    // Track initial page view
    trackPageView();
    
    // Initialize all tracking modules
    trackClicks();
    trackFormInteractions();
    trackTimeOnPage();
    trackMouseMovements();
    trackKeyboardInteractions();
    trackWindowResize();
    trackVisibilityChanges();
    
    // Retry any failed events
    retryFailedEvents();
    
    console.log('Clickstream tracking initialized');
}

// Initialize tracking when DOM is loaded
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeTracking);
} else {
    initializeTracking();
}

// Export functions for use in other scripts
window.clickstreamTracking = {
    trackEvent: trackEvent,
    trackPageView: trackPageView,
    retryFailedEvents: retryFailedEvents
};
