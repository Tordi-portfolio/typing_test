let startTime = null;
let timerInterval = null;
let testActive = false;
const testWordsElement = document.getElementById('testWords');
const typingInput = document.getElementById('typingInput');
const resultsBox = document.getElementById('resultsBox');

typingInput.addEventListener('input', function() {
    if (!testActive) {
        testActive = true;
        startTime = Date.now();
        startTimer();
    }
    
    updateDisplay();
    calculateStats();
});

function startTimer() {
    timerInterval = setInterval(() => {
        const elapsed = Math.floor((Date.now() - startTime) / 1000);
        document.getElementById('timer').textContent = elapsed + 's';
    }, 100);
}

function updateDisplay() {
    const originalText = testWordsElement.textContent;
    const typedText = typingInput.value;
    
    let displayHTML = '';
    for (let i = 0; i < originalText.length; i++) {
        if (i < typedText.length) {
            if (typedText[i] === originalText[i]) {
                displayHTML += '<span class="correct">' + originalText[i] + '</span>';
            } else {
                displayHTML += '<span class="incorrect">' + originalText[i] + '</span>';
            }
        } else if (i === typedText.length) {
            displayHTML += '<span class="current">' + originalText[i] + '</span>';
        } else {
            displayHTML += originalText[i];
        }
    }
    testWordsElement.innerHTML = displayHTML;
}

function calculateStats() {
    const originalText = testWordsElement.textContent;
    const typedText = typingInput.value;
    
    let errors = 0;
    for (let i = 0; i < Math.max(originalText.length, typedText.length); i++) {
        if (i >= originalText.length || i >= typedText.length || originalText[i] !== typedText[i]) {
            errors++;
        }
    }
    
    const elapsed = Math.floor((Date.now() - startTime) / 1000);
    const wordsTyped = typedText.split(/\s+/).filter(w => w.length > 0).length;
    const wpm = elapsed > 0 ? Math.round((wordsTyped / elapsed) * 60) : 0;
    
    const accuracy = originalText.length > 0 ? Math.max(0, Math.round(((originalText.length - errors) / originalText.length) * 100)) : 0;
    
    document.getElementById('wpm').textContent = wpm;
    document.getElementById('accuracy').textContent = accuracy + '%';
    document.getElementById('errors').textContent = errors;
    
    if (typedText.trim().length > 0 && typedText.length >= originalText.length) {
        completeTest(wpm, accuracy, errors, elapsed);
    }
}

function completeTest(wpm, accuracy, errors, elapsed) {
    testActive = false;
    clearInterval(timerInterval);
    typingInput.disabled = true;
    
    document.getElementById('finalWpm').textContent = wpm;
    document.getElementById('finalAccuracy').textContent = accuracy + '%';
    document.getElementById('finalErrors').textContent = errors;
    resultsBox.style.display = 'block';
    
    fetch('/calculate/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({
            original_text: testWordsElement.textContent,
            typed_text: typingInput.value,
            time_taken: elapsed,
            difficulty: currentDifficulty
        })
    }).then(response => response.json())
      .then(data => console.log('Result saved:', data))
      .catch(error => console.error('Error:', error));
}

function resetTest() {
    testActive = false;
    clearInterval(timerInterval);
    typingInput.value = '';
    typingInput.disabled = false;
    resultsBox.style.display = 'none';
    startTime = null;
    
    document.getElementById('timer').textContent = '0s';
    document.getElementById('wpm').textContent = '0';
    document.getElementById('accuracy').textContent = '0%';
    document.getElementById('errors').textContent = '0';
    
    updateDisplay();
    typingInput.focus();
}

function newTest() {
    fetch('/new-test/?difficulty=' + currentDifficulty)
        .then(response => response.json())
        .then(data => {
            testWordsElement.textContent = data.words;
            resetTest();
        })
        .catch(error => console.error('Error:', error));
}

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

window.addEventListener('load', () => {
    typingInput.focus();
});