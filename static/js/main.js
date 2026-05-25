function toggleDarkMode() {
    document.body.classList.toggle('dark');
    localStorage.setItem('darkMode', document.body.classList.contains('dark'));
}

function toggleFocusMode() {
    document.body.classList.toggle('focus-mode');
}

function showThemeMenu() {
    document.getElementById('themeMenu').classList.remove('hidden');
}

function hideThemeMenu() {
    document.getElementById('themeMenu').classList.add('hidden');
}

function setTheme(theme) {
    document.body.className = document.body.className.replace(/theme-\w+/g, '');
    if (theme !== 'default') {
        document.body.classList.add(`theme-${theme}`);
    }
    localStorage.setItem('currentTheme', theme);
    hideThemeMenu();
}

// Initialization
if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark');
const savedTheme = localStorage.getItem('currentTheme');
if (savedTheme) setTheme(savedTheme);

// Progress Logic
function updateGoalDisplay(words) {
    const goal = 500;
    const progress = Math.min(100, (words / goal) * 100);
    const bar = document.getElementById('goalBar');
    const text = document.getElementById('goalText');
    if (bar) bar.style.width = `${progress}%`;
    if (text) text.innerText = `${words}/${goal} words`;
}

// WPM Tracker
let startTypingTime = null;
let initialWordCount = 0;

function trackWPM(currentText) {
    if (!currentText.trim()) {
        startTypingTime = null;
        document.getElementById('wpmValue').innerText = '0';
        return;
    }
    if (!startTypingTime) {
        startTypingTime = new Date();
        initialWordCount = currentText.trim().split(/\s+/).length;
    }
    const now = new Date();
    const minutes = (now - startTypingTime) / 1000 / 60;
    if (minutes > 0.05) {
        const currentWords = currentText.trim().split(/\s+/).length;
        const diff = Math.max(0, currentWords - initialWordCount);
        const wpm = Math.round(diff / minutes);
        document.getElementById('wpmValue').innerText = wpm;
    }
}
