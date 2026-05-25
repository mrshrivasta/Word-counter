function toggleDarkMode() {
    document.body.classList.toggle('dark');
    localStorage.setItem('darkMode', document.body.classList.contains('dark'));
}

function toggleFocusMode() {
    document.body.classList.toggle('focus-mode');
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    sidebar.classList.toggle('sidebar-collapsed');
    document.querySelectorAll('.nav-text, .logo-text').forEach(el => el.classList.toggle('hidden'));
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

// Init
if (localStorage.getItem('darkMode') === 'true') document.body.classList.add('dark');
const savedTheme = localStorage.getItem('currentTheme');
if (savedTheme) setTheme(savedTheme);

// Streak & Goals
let dailyGoal = 500;
function updateGoalDisplay(words) {
    const progress = Math.min(100, (words / dailyGoal) * 100);
    const bar = document.getElementById('goalBar');
    const text = document.getElementById('goalText');
    if (bar) bar.style.width = `${progress}%`;
    if (text) text.innerText = `${words}/${dailyGoal}`;

    if (progress >= 100 && bar) bar.classList.replace('bg-green-500', 'bg-indigo-500');
}

// Global WPM Tracker
let startTypingTime = null;
let initialWordCount = 0;

function trackWPM(currentText) {
    if (!startTypingTime) {
        startTypingTime = new Date();
        initialWordCount = currentText.trim().split(/\s+/).length;
        return;
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
