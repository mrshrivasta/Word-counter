const editor = document.getElementById('editor');
const footWords = document.getElementById('footWords');
const footChars = document.getElementById('footChars');
const footRead = document.getElementById('footRead');
const autosaveStatus = document.getElementById('autosaveStatus');

let debounceTimer;

if (editor) {
    editor.addEventListener('input', () => {
        const text = editor.value;

        // Update basic footer stats immediately
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        if (footWords) footWords.innerText = words;
        if (footChars) footChars.innerText = text.length;
        if (footRead) footRead.innerText = Math.ceil(words / 225) + 'm';

        updateGoalDisplay(words);
        trackWPM(text);

        // Debounce advanced analysis
        autosaveStatus.innerHTML = '<i class="fas fa-spinner fa-spin mr-1"></i> Saving...';
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            performAnalysis(text);
            localStorage.setItem('editor_content', text);
        }, 800);
    });

    // Load initial
    const saved = localStorage.getItem('editor_content');
    if (saved) {
        editor.value = saved;
        performAnalysis(saved);
    }
}

async function performAnalysis(text) {
    if (!text.trim()) {
        autosaveStatus.innerHTML = '<i class="fas fa-check-circle mr-1"></i> Ready';
        return;
    }

    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });
        const data = await response.json();

        document.getElementById('latencyDisplay').innerText = `Latency: ${data.processing_time}ms`;
        autosaveStatus.innerHTML = `<i class="fas fa-check-circle mr-1"></i> Saved ${new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}`;

        // Dispatch to page-specific scripts
        const event = new CustomEvent('analysisData', { detail: data });
        document.dispatchEvent(event);

    } catch (e) {
        console.error("Analysis failed", e);
        autosaveStatus.innerHTML = '<i class="fas fa-exclamation-circle text-red-500 mr-1"></i> Error';
    }
}

// Keyboard Shortcuts
document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 's') {
        e.preventDefault();
        performAnalysis(editor.value);
    }
    if (e.ctrlKey && e.key === '/') {
        e.preventDefault();
        toggleFocusMode();
    }
    if (e.ctrlKey && e.key === 'Enter') {
        e.preventDefault();
        performAnalysis(editor.value);
    }
});

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

function copyText() {
    editor.select();
    document.execCommand('copy');
}

function clearText() {
    if (confirm('Clear everything?')) {
        editor.value = '';
        localStorage.removeItem('editor_content');
        performAnalysis('');
    }
}
