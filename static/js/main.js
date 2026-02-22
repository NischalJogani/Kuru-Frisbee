// Frisbee Tracker - Main JavaScript

// Loading Screen
window.addEventListener('load', function() {
    const loadingScreen = document.getElementById('loading-screen');
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.classList.add('hidden');
            setTimeout(() => {
                loadingScreen.style.display = 'none';
            }, 500);
        }, 500);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    initApp();
    initDarkMode();
    initHamburgerMenu();
});

function initApp() {
    // Add confirmation dialogs for delete actions
    setupDeleteConfirmations();
    
    // Setup live score updates if on a match page
    setupLiveUpdates();
    
    // Setup form validations
    setupFormValidations();
    
    // Add smooth scrolling
    setupSmoothScrolling();
    
    // Auto-dismiss flash messages
    setupFlashMessages();
}

// Hamburger Menu for Mobile
function initHamburgerMenu() {
    const hamburger = document.getElementById('hamburger');
    const navLinks = document.getElementById('navLinks');
    
    if (!hamburger || !navLinks) return;
    
    hamburger.addEventListener('click', function() {
        navLinks.classList.toggle('active');
        hamburger.classList.toggle('active');
    });
    
    // Close menu when clicking a link
    const links = navLinks.querySelectorAll('a');
    links.forEach(link => {
        link.addEventListener('click', function() {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        });
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', function(event) {
        if (!hamburger.contains(event.target) && !navLinks.contains(event.target)) {
            navLinks.classList.remove('active');
            hamburger.classList.remove('active');
        }
    });
}

// Dark Mode Management
function initDarkMode() {
    const themeToggle = document.getElementById('theme-toggle');
    if (!themeToggle) return;
    
    // Load saved theme or default to light
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
    
    themeToggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        
        // Add animation
        this.style.transform = 'rotate(360deg)';
        setTimeout(() => {
            this.style.transform = 'rotate(0deg)';
        }, 300);
    });
}

// Flash messages auto-dismiss
function setupFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.animation = 'slideOutRight 0.3s ease-out';
            setTimeout(() => msg.remove(), 300);
        }, 5000);
    });
}

// Setup delete confirmations
function setupDeleteConfirmations() {
    const deleteForms = document.querySelectorAll('form[action*="delete"]');
    deleteForms.forEach(form => {
        if (!form.hasAttribute('onsubmit')) {
            form.addEventListener('submit', function(e) {
                const itemType = this.action.includes('team') ? 'team' : 
                               this.action.includes('player') ? 'player' : 
                               this.action.includes('match') ? 'match' : 'item';
                if (!confirm(`Are you sure you want to delete this ${itemType}?`)) {
                    e.preventDefault();
                }
            });
        }
    });
}

// Setup live score updates for match detail pages
function setupLiveUpdates() {
    const matchDetailPage = document.querySelector('.match-detail-container');
    const scoringPage = document.querySelector('.scoring-container');
    
    if (matchDetailPage) {
        // Check if match is live
        const liveStatus = document.querySelector('.match-status-badge.live');
        if (liveStatus) {
            startLiveScoreUpdates();
        }
    }
    
    if (scoringPage) {
        // Auto-refresh player stats every 5 seconds without reloading the page
        // This allows modals to stay open while updating data
        // The updateLiveData() function from the template will handle this
    }
}

// Live score updates via AJAX
function startLiveScoreUpdates() {
    const matchId = getMatchIdFromURL();
    if (!matchId) return;
    
    setInterval(() => {
        fetchMatchScores(matchId);
    }, 3000); // Update every 3 seconds
}

function getMatchIdFromURL() {
    const path = window.location.pathname;
    const matches = path.match(/\/match\/(\d+)/);
    return matches ? matches[1] : null;
}

function fetchMatchScores(matchId) {
    fetch(`/api/match/${matchId}/scores`)
        .then(response => response.json())
        .then(data => {
            updateScoreboard(data);
            updateTimeline(data.scores);
        })
        .catch(error => {
            console.error('Error fetching scores:', error);
        });
}

function updateScoreboard(data) {
    const scoreElements = document.querySelectorAll('.live-score');
    if (scoreElements.length >= 2) {
        scoreElements[0].textContent = data.team1_score;
        scoreElements[1].textContent = data.team2_score;
        
        // Add animation
        scoreElements.forEach(el => {
            el.classList.add('score-update');
            setTimeout(() => el.classList.remove('score-update'), 500);
        });
    }
}

function updateTimeline(scores) {
    const timeline = document.getElementById('timeline');
    if (!timeline) return;
    
    if (scores.length === 0) {
        timeline.innerHTML = '<div class="empty-state">No scores yet in this match.</div>';
        return;
    }
    
    timeline.innerHTML = scores.map(score => `
        <div class="timeline-item">
            <div class="timeline-time">${score.timestamp}</div>
            <div class="timeline-content">
                <div class="scorer-info">
                    <strong>${score.player_name}</strong>
                    <span class="scorer-team">(${score.team_name})</span>
                </div>
                <div class="score-value">+${score.points} point${score.points !== 1 ? 's' : ''}</div>
            </div>
        </div>
    `).join('');
}

// Form validations
function setupFormValidations() {
    // Match form validation
    const matchForm = document.querySelector('.match-form');
    if (matchForm) {
        matchForm.addEventListener('submit', function(e) {
            const team1 = this.querySelector('[name="team1_id"]').value;
            const team2 = this.querySelector('[name="team2_id"]').value;
            
            if (team1 === team2) {
                e.preventDefault();
                alert('Team 1 and Team 2 must be different!');
                return false;
            }
        });
    }
    
    // Player form validation
    const playerForm = document.querySelector('.player-form');
    if (playerForm) {
        playerForm.addEventListener('submit', function(e) {
            const name = this.querySelector('[name="name"]').value.trim();
            if (name.length < 2) {
                e.preventDefault();
                alert('Player name must be at least 2 characters long!');
                return false;
            }
        });
    }
}

// Smooth scrolling for anchor links
function setupSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Helper function to format dates
function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Helper function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${type === 'success' ? '#22c55e' : type === 'error' ? '#ef4444' : '#2563eb'};
        color: white;
        border-radius: 0.5rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
    
    .score-update {
        animation: scoreFlash 0.5s ease-in-out;
    }
    
    @keyframes scoreFlash {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
            color: var(--success-color);
        }
    }
`;
document.head.appendChild(style);

// Export functions for use in other scripts
window.FrisbeeTracker = {
    updateScoreboard,
    updateTimeline,
    showNotification,
    formatDate
};
