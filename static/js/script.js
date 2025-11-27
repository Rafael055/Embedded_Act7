document.addEventListener('DOMContentLoaded', function () {
  // Elements
  const langEnglish = document.getElementById('langEnglish');
  const langTagalog = document.getElementById('langTagalog');
  const voiceBtn = document.getElementById('voiceBtn');
  const voiceBtnText = document.getElementById('voiceBtnText');
  const recognizedText = document.getElementById('recognizedText');
  const commandStatus = document.getElementById('commandStatus');
  const notification = document.getElementById('notification');
  const notificationText = document.getElementById('notificationText');
  const closeNotification = document.getElementById('closeNotification');
  const commandsEnglish = document.getElementById('commandsEnglish');
  const commandsTagalog = document.getElementById('commandsTagalog');
  const commandsHelpTitle = document.getElementById('commandsHelpTitle');

  // LED icons
  const whiteLedIcon = document.getElementById('whiteLedIcon');
  const blueLedIcon = document.getElementById('blueLedIcon');
  const redLedIcon = document.getElementById('redLedIcon');
  const buzzerIcon = document.getElementById('buzzerIcon');

  // State
  let currentLanguage = 'en-US';
  let isListening = false;
  let recognition = null;

  // Translations
  const translations = {
    'en-US': {
      voiceControl: 'Voice Control',
      startListening: 'Start Listening',
      stopListening: 'Stop Listening',
      listening: 'Listening...',
      ledControls: 'LED Controls',
      allOn: 'All ON',
      allOff: 'All OFF',
      commandsHelp: 'Available Commands:'
    },
    'fil-PH': {
      voiceControl: 'Kontrol ng Boses',
      startListening: 'Makinig',
      stopListening: 'Itigil',
      listening: 'Nakikinig...',
      ledControls: 'Kontrol ng LED',
      allOn: 'Lahat ON',
      allOff: 'Lahat OFF',
      commandsHelp: 'Mga Available na Utos:'
    }
  };

  // Initialize Web Speech API
  if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;

    recognition.onstart = function () {
      isListening = true;
      voiceBtn.classList.add('listening');
      voiceBtnText.textContent = translations[currentLanguage].listening;
      recognizedText.textContent = '';
      commandStatus.textContent = '';
      commandStatus.className = 'command-status';
    };

    recognition.onend = function () {
      isListening = false;
      voiceBtn.classList.remove('listening');
      voiceBtnText.textContent = translations[currentLanguage].startListening;
    };

    recognition.onresult = function (event) {
      const transcript = event.results[0][0].transcript;
      recognizedText.textContent = `"${transcript}"`;
      processVoiceCommand(transcript);
    };

    recognition.onerror = function (event) {
      console.error('Speech recognition error:', event.error);
      isListening = false;
      voiceBtn.classList.remove('listening');
      voiceBtnText.textContent = translations[currentLanguage].startListening;

      if (event.error === 'no-speech') {
        commandStatus.textContent = 'No speech detected. Please try again.';
      } else if (event.error === 'not-allowed') {
        commandStatus.textContent = 'Microphone access denied. Please allow microphone access.';
      } else {
        commandStatus.textContent = `Error: ${event.error}`;
      }
      commandStatus.className = 'command-status error';
    };
  } else {
    voiceBtn.disabled = true;
    voiceBtnText.textContent = 'Speech not supported';
    console.warn('Web Speech API not supported');
  }

  // Voice button click
  voiceBtn.addEventListener('click', function () {
    if (!recognition) return;

    if (isListening) {
      recognition.stop();
    } else {
      recognition.lang = currentLanguage;
      recognition.start();
    }
  });

  // Language selection
  langEnglish.addEventListener('click', function () {
    setLanguage('en-US');
  });

  langTagalog.addEventListener('click', function () {
    setLanguage('fil-PH');
  });

  function setLanguage(lang) {
    currentLanguage = lang;

    // Update UI
    langEnglish.classList.toggle('active', lang === 'en-US');
    langTagalog.classList.toggle('active', lang === 'fil-PH');

    // Update text
    const t = translations[lang];
    document.getElementById('voiceTitle').textContent = t.voiceControl;
    voiceBtnText.textContent = isListening ? t.listening : t.startListening;
    document.getElementById('ledTitle').textContent = t.ledControls;
    document.getElementById('allOnText').textContent = t.allOn;
    document.getElementById('allOffText').textContent = t.allOff;
    commandsHelpTitle.textContent = t.commandsHelp;

    // Show/hide command lists
    commandsEnglish.classList.toggle('hidden', lang !== 'en-US');
    commandsTagalog.classList.toggle('hidden', lang !== 'fil-PH');

    // Show/hide Tagalog labels
    document.querySelectorAll('.led-label-tagalog').forEach(el => {
      el.classList.toggle('hidden', lang !== 'fil-PH');
    });

    // Save to server
    fetch('/api/set_language', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ language: lang })
    });
  }

  // Process voice command
  async function processVoiceCommand(text) {
    try {
      const response = await fetch('/api/voice_command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: text, language: currentLanguage })
      });

      const data = await response.json();

      if (data.success) {
        commandStatus.textContent = `✓ Command executed: ${formatAction(data.action)}`;
        commandStatus.className = 'command-status success';
        updateLEDStates(data.states);
      } else if (data.invalid_color) {
        // Show notification for invalid color
        showNotification(data.message);
        commandStatus.textContent = `✗ ${data.message}`;
        commandStatus.className = 'command-status error';

        // Trigger buzzer animation
        buzzerIcon.classList.add('on');
        setTimeout(() => buzzerIcon.classList.remove('on'), 500);
      } else {
        commandStatus.textContent = `✗ ${data.error || 'Command not recognized'}`;
        commandStatus.className = 'command-status error';
      }

      if (data.states) {
        updateLEDStates(data.states);
      }
    } catch (error) {
      console.error('Error processing command:', error);
      commandStatus.textContent = '✗ Error processing command';
      commandStatus.className = 'command-status error';
    }
  }

  function formatAction(action) {
    const actionLabels = {
      'white_on': 'White LED ON',
      'white_off': 'White LED OFF',
      'blue_on': 'Blue LED ON',
      'blue_off': 'Blue LED OFF',
      'red_on': 'Red LED ON',
      'red_off': 'Red LED OFF',
      'all_on': 'All LEDs ON',
      'all_off': 'All LEDs OFF',
      'buzzer': 'Buzzer activated'
    };
    return actionLabels[action] || action;
  }

  // Update LED visual states
  function updateLEDStates(states) {
    whiteLedIcon.classList.toggle('on', states.white);
    blueLedIcon.classList.toggle('on', states.blue);
    redLedIcon.classList.toggle('on', states.red);

    if (states.buzzer) {
      buzzerIcon.classList.add('on');
      setTimeout(() => buzzerIcon.classList.remove('on'), 300);
    }
  }

  // LED button controls
  document.querySelectorAll('.led-btn').forEach(btn => {
    btn.addEventListener('click', async function () {
      const led = this.dataset.led;
      const action = this.dataset.action;

      try {
        const response = await fetch(`/api/led/${led}/${action}`, {
          method: 'POST'
        });
        const data = await response.json();

        if (data.success) {
          updateLEDStates(data.states);

          // Animate buzzer if clicked
          if (led === 'buzzer') {
            buzzerIcon.classList.add('on');
            setTimeout(() => buzzerIcon.classList.remove('on'), 300);
          }
        }
      } catch (error) {
        console.error('Error controlling LED:', error);
      }
    });
  });

  // All ON/OFF buttons
  document.getElementById('allOnBtn').addEventListener('click', async function () {
    try {
      const response = await fetch('/api/led/all/on', { method: 'POST' });
      const data = await response.json();
      if (data.success) {
        updateLEDStates(data.states);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

  document.getElementById('allOffBtn').addEventListener('click', async function () {
    try {
      const response = await fetch('/api/led/all/off', { method: 'POST' });
      const data = await response.json();
      if (data.success) {
        updateLEDStates(data.states);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

  // Notification
  function showNotification(message) {
    notificationText.textContent = message;
    notification.classList.remove('hidden');

    // Auto-hide after 5 seconds
    setTimeout(() => {
      notification.classList.add('hidden');
    }, 5000);
  }

  closeNotification.addEventListener('click', function () {
    notification.classList.add('hidden');
  });

  // Initial state fetch
  async function fetchInitialState() {
    try {
      const response = await fetch('/api/states');
      const data = await response.json();
      if (data.success) {
        updateLEDStates(data.states);
      }
    } catch (error) {
      console.error('Error fetching initial state:', error);
    }
  }

  fetchInitialState();
});
