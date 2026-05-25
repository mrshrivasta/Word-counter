const editor = document.getElementById('editor');
const footWords = document.getElementById('footWords');
const footChars = document.getElementById('footChars');
const footRead = document.getElementById('footRead');
const latencyDisplay = document.getElementById('latencyDisplay');
const saveIndicator = document.getElementById('saveIndicator');

let debounceTimer;

if (editor) {
    editor.addEventListener('input', () => {
        const text = editor.value;

        // Instant updates
        const words = text.trim() ? text.trim().split(/\s+/).length : 0;
        if (footWords) footWords.innerText = words;
        if (footChars) footChars.innerText = text.length;
        if (footRead) footRead.innerText = Math.ceil(words / 225) + 'm';

        updateGoalDisplay(words);
        trackWPM(text);

        // Analysis debounce
        saveIndicator.innerHTML = '<i class="fas fa-spinner fa-spin mr-2"></i> Analyzing...';
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            triggerFullAnalysis(text);
        }, 1000);
    });

    // Initial Load
    const saved = localStorage.getItem('wc_draft');
    if (saved) {
        editor.value = saved;
        triggerFullAnalysis(saved);
    }
}

async function triggerFullAnalysis(text) {
    if (!text.trim()) {
        saveIndicator.innerHTML = '<i class="fas fa-circle text-[6px] mr-2 text-green-500"></i> Synced Local';
        return;
    }

    try {
        const res = await fetch('/api/analyze', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({text})
        });
        const data = await res.json();

        localStorage.setItem('wc_draft', text);
        if (latencyDisplay) latencyDisplay.innerText = `Engine: ${data.processing_time}ms`;
        saveIndicator.innerHTML = `<i class="fas fa-check-circle mr-2 text-indigo-500"></i> Saved ${new Date().toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}`;

        // Dispatch to page specific logic
        document.dispatchEvent(new CustomEvent('engineReady', { detail: data }));
    } catch (e) {
        saveIndicator.innerHTML = '<i class="fas fa-exclamation-triangle mr-2 text-red-500"></i> Error';
    }
}

// Shortcuts
document.addEventListener('keydown', e => {
    if (e.ctrlKey && e.key === 's') { e.preventDefault(); triggerFullAnalysis(editor.value); }
    if (e.ctrlKey && e.key === '/') { e.preventDefault(); toggleFocusMode(); }
});

// Export Utils
async function exportFile(format) {
    const res = await fetch(`/api/export/${format}`, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({text: editor.value})
    });
    if (res.ok) {
        const blob = await res.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `wc_export.${format}`;
        a.click();
    }
}
