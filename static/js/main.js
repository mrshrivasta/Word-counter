// Dark Mode Toggle
const darkModeToggle = document.getElementById('darkModeToggle');
const body = document.body;

if (localStorage.getItem('darkMode') === 'enabled') {
    body.classList.add('dark');
}

if (darkModeToggle) {
    darkModeToggle.addEventListener('click', () => {
        body.classList.toggle('dark');
        if (body.classList.contains('dark')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });
}

// Focus Mode Toggle
const focusModeToggle = document.getElementById('focusModeToggle');
if (focusModeToggle) {
    focusModeToggle.addEventListener('click', () => {
        body.classList.toggle('focus-mode');
    });
}

// Global state for streak and goals
document.getElementById('streakCount').innerText = localStorage.getItem('writingStreak') || 0;
let dailyGoal = 500;
let currentWordsTotal = 0;

function updateGoalDisplay(words) {
    currentWordsTotal = words;
    const goalProgress = document.getElementById('goalProgress');
    if (goalProgress) {
        goalProgress.innerText = `${currentWordsTotal}/${dailyGoal}`;
        if (currentWordsTotal >= dailyGoal) {
            document.getElementById('goalDisplay').classList.add('text-green-600', 'font-bold');
        }
    }
}

// Pomodoro Timer
let pomoInterval;
let pomoTime = 25 * 60;
let isPomoRunning = false;

function togglePomo() {
    const btn = document.querySelector('#pomodoroDisplay button');
    if (isPomoRunning) {
        clearInterval(pomoInterval);
        btn.innerText = 'Start';
    } else {
        pomoInterval = setInterval(updatePomo, 1000);
        btn.innerText = 'Pause';
    }
    isPomoRunning = !isPomoRunning;
}

function updatePomo() {
    pomoTime--;
    if (pomoTime <= 0) {
        clearInterval(pomoInterval);
        alert('Time is up! Take a break.');
        pomoTime = 25 * 60;
        isPomoRunning = false;
        document.querySelector('#pomodoroDisplay button').innerText = 'Start';
    }
    const mins = Math.floor(pomoTime / 60);
    const secs = pomoTime % 60;
    document.getElementById('pomoTimer').innerText = `${mins}:${secs.toString().padStart(2, '0')}`;
}
