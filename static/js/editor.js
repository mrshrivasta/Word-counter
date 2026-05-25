const editor = document.getElementById('editor');
const footerWords = document.getElementById('footerWords');
const footerChars = document.getElementById('footerChars');
const footerReading = document.getElementById('footerReading');
const typingStatus = document.getElementById('typingStatus');

let typingTimer;
const typingDelay = 1000;

let startTime;
let wordCountAtStart = 0;

if (editor) {
    editor.addEventListener('input', () => {
        const text = editor.value;
        updateBasicStats(text);

        if (!startTime) {
            startTime = new Date();
            const words = text.trim() ? text.trim().split(/\s+/).length : 0;
            wordCountAtStart = words;
        }

        updateWPM(text);

        clearTimeout(typingTimer);
        typingStatus.innerText = 'Typing...';
        typingTimer = setTimeout(() => {
            analyzeText(text);
            typingStatus.innerText = 'Saved';
            localStorage.setItem('editorContent', text);
        }, typingDelay);
    });

    // Load saved content
    const savedContent = localStorage.getItem('editorContent');
    if (savedContent) {
        editor.value = savedContent;
        updateBasicStats(savedContent);
        analyzeText(savedContent);
    }
}

function updateWPM(text) {
    if (!startTime) return;
    const currentTime = new Date();
    const timeElapsed = (currentTime - startTime) / 1000 / 60; // in minutes
    if (timeElapsed > 0.05) { // Update after 3 seconds of typing
        const currentWords = text.trim() ? text.trim().split(/\s+/).length : 0;
        const wordsTyped = Math.max(0, currentWords - wordCountAtStart);
        const wpm = Math.round(wordsTyped / timeElapsed);
        const wpmDisplay = document.getElementById('wpmCount');
        if (wpmDisplay) wpmDisplay.innerText = wpm;
    }
}

function updateBasicStats(text) {
    const words = text.trim() ? text.trim().split(/\s+/).length : 0;
    const chars = text.length;
    const readingTime = Math.ceil(words / 225);

    if (footerWords) footerWords.innerText = words;
    if (footerChars) footerChars.innerText = chars;
    if (footerReading) footerReading.innerText = readingTime + 'm';

    if (typeof updateGoalDisplay === 'function') {
        updateGoalDisplay(words);
    }
}

async function analyzeText(text) {
    if (!text.trim()) return;

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        updateDashboard(data);
    } catch (error) {
        console.error('Error analyzing text:', error);
    }
}

function updateDashboard(data) {
    const event = new CustomEvent('analysisUpdate', { detail: data });
    document.dispatchEvent(event);
}

// Export functions
async function exportFile(format) {
    const text = editor.value;
    const response = await fetch(`/api/export/${format}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });

    if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `document.${format}`;
        document.body.appendChild(a);
        a.click();
        a.remove();
    }
}

function clearText() {
    if (confirm('Clear all text?')) {
        editor.value = '';
        updateBasicStats('');
        localStorage.removeItem('editorContent');
        startTime = null;
    }
}

function copyText() {
    editor.select();
    document.execCommand('copy');
}
