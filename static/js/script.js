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
  const aiLanguage = document.getElementById('aiLanguage');

  // LED icons
  const whiteLedIcon = document.getElementById('whiteLedIcon');
  const blueLedIcon = document.getElementById('blueLedIcon');
  const redLedIcon = document.getElementById('redLedIcon');
  const buzzerIcon = document.getElementById('buzzerIcon');

  // Voice selection elements
  const voiceMaleBtn = document.getElementById('voiceMale');
  const voiceFemaleBtn = document.getElementById('voiceFemale');
  const testVoiceBtn = document.getElementById('testVoiceBtn');

  // Robot elements
  const robotLeftEye = document.getElementById('robotLeftEye');
  const robotRightEye = document.getElementById('robotRightEye');
  const robotNose = document.getElementById('robotNose');
  const robotMouth = document.getElementById('robotMouth');
  const robotMessage = document.getElementById('robotMessage');
  const antennaLight = document.getElementById('antennaLight');
  const robotTemp = document.getElementById('robotTemp');
  const robotHumidity = document.getElementById('robotHumidity');
  const robotStatus = document.getElementById('robotStatus');
  const robotStatusTagalog = document.getElementById('robotStatusTagalog');

  // State
  let currentLanguage = 'en-US';
  let currentVoiceType = 'male'; // 'male' or 'female'
  let isListening = false;
  let recognition = null;
  let synthesis = window.speechSynthesis;
  let voices = [];

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
      allBlink: 'Blink All',
      commandsHelp: 'Available Commands:',
      dhtTitle: 'Temperature & Humidity',
      dhtFetching: 'Fetching sensor data...',
      dhtUpdated: 'Last updated:',
      dhtError: 'Error reading sensor',
      voiceSelectTitle: 'Voice Assistant',
      maleVoice: 'Male Voice',
      femaleVoice: 'Female Voice',
      testVoice: 'Test Voice',
      robotTitle: 'Mini-Bot Assistant',
      robotReady: 'Ready to assist!',
      robotListening: 'Listening...',
      robotExecuted: 'Command executed!',
      robotError: 'Command not recognized',
      testMessage: 'Hello! I am your voice assistant. How can I help you today?'
    },
    'fil-PH': {
      voiceControl: 'Kontrol ng Boses',
      startListening: 'Makinig',
      stopListening: 'Itigil',
      listening: 'Nakikinig...',
      ledControls: 'Kontrol ng LED',
      allOn: 'Lahat ON',
      allOff: 'Lahat OFF',
      allBlink: 'Kumukurap Lahat',
      commandsHelp: 'Mga maaring i-utos:',
      dhtTitle: 'Temperatura at Halumigmig',
      dhtFetching: 'Kinukuha ang datos...',
      dhtUpdated: 'Huling update:',
      dhtError: 'Error sa pagbasa ng sensor',
      voiceSelectTitle: 'Boses ng Assistant',
      maleVoice: 'Boses Lalaki',
      femaleVoice: 'Boses Babae',
      testVoice: 'Subukan ang Boses',
      robotTitle: 'Mini-Bot na Katulong',
      robotReady: 'Handa na ako!',
      robotListening: 'Nakikinig...',
      robotExecuted: 'Naisakatuparan ang utos!',
      robotError: 'Hindi maintindihan ang utos',
      testMessage: 'Kamusta! Ako ang iyong voice assistant. Paano kita matutulungan?'
    }
  };

  // Load available voices
  function loadVoices() {
    voices = synthesis.getVoices();
  }

  loadVoices();
  if (synthesis.onvoiceschanged !== undefined) {
    synthesis.onvoiceschanged = loadVoices;
  }

  // Get appropriate voice based on language and type
  function getVoice() {
    const langCode = currentLanguage === 'en-US' ? 'en' : 'fil';
    const preferFemale = currentVoiceType === 'female';

    // Try to find a matching voice
    let selectedVoice = null;

    // First, try to find exact language match with gender preference
    for (let voice of voices) {
      const isEnglish = voice.lang.startsWith('en');
      const isFemale = voice.name.toLowerCase().includes('female') ||
        voice.name.toLowerCase().includes('woman') ||
        voice.name.toLowerCase().includes('zira') ||
        voice.name.toLowerCase().includes('samantha') ||
        voice.name.toLowerCase().includes('victoria') ||
        voice.name.toLowerCase().includes('karen') ||
        voice.name.toLowerCase().includes('moira');

      if (currentLanguage === 'en-US' && isEnglish) {
        if (preferFemale === isFemale) {
          selectedVoice = voice;
          break;
        } else if (!selectedVoice) {
          selectedVoice = voice;
        }
      } else if (currentLanguage === 'fil-PH') {
        // For Filipino, fall back to English voices since Filipino TTS is limited
        if (isEnglish) {
          if (preferFemale === isFemale) {
            selectedVoice = voice;
            break;
          } else if (!selectedVoice) {
            selectedVoice = voice;
          }
        }
      }
    }

    return selectedVoice;
  }

  // Speak text using TTS
  function speak(text, callback) {
    if (!synthesis) return;

    synthesis.cancel(); // Cancel any ongoing speech

    const utterance = new SpeechSynthesisUtterance(text);
    const voice = getVoice();

    if (voice) {
      utterance.voice = voice;
    }

    utterance.lang = currentLanguage === 'fil-PH' ? 'en-US' : currentLanguage;
    utterance.rate = currentVoiceType === 'male' ? 0.9 : 1.0;
    utterance.pitch = currentVoiceType === 'male' ? 0.8 : 1.2;

    // Animate robot mouth while speaking
    utterance.onstart = () => {
      robotMouth.classList.add('speaking');
      antennaLight.classList.add('active');
    };

    utterance.onend = () => {
      robotMouth.classList.remove('speaking');
      antennaLight.classList.remove('active');
      if (callback) callback();
    };

    synthesis.speak(utterance);
  }

  // Update robot display
  function updateRobotMessage(message) {
    robotMessage.textContent = message;
  }

  function updateRobotStatus(status, isTagalog = false) {
    const t = translations[currentLanguage];
    robotStatus.textContent = status;
    if (currentLanguage === 'fil-PH') {
      robotStatusTagalog.classList.remove('hidden');
    } else {
      robotStatusTagalog.classList.add('hidden');
    }
  }

  // Robot eye blinking animation
  function robotBlink() {
    robotLeftEye.classList.add('blinking');
    robotRightEye.classList.add('blinking');
    setTimeout(() => {
      robotLeftEye.classList.remove('blinking');
      robotRightEye.classList.remove('blinking');
    }, 300);
  }

  // Random blinking every 5 seconds
  setInterval(() => {
    if (Math.random() > 0.5) {
      robotBlink();
    }
  }, 5000);

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

      // Update robot
      const t = translations[currentLanguage];
      updateRobotMessage(t.robotListening);
      updateRobotStatus(t.robotListening);
      antennaLight.classList.add('active');
    };

    recognition.onend = function () {
      isListening = false;
      voiceBtn.classList.remove('listening');
      voiceBtnText.textContent = translations[currentLanguage].startListening;
      antennaLight.classList.remove('active');
    };

    recognition.onresult = function (event) {
      const transcript = event.results[0][0].transcript;
      recognizedText.textContent = `"${transcript}"`;
      updateRobotMessage(`"${transcript}"`);
      processVoiceCommand(transcript);
    };

    recognition.onerror = function (event) {
      console.error('Speech recognition error:', event.error);
      isListening = false;
      voiceBtn.classList.remove('listening');
      voiceBtnText.textContent = translations[currentLanguage].startListening;
      antennaLight.classList.remove('active');

      if (event.error === 'no-speech') {
        commandStatus.textContent = 'No speech detected. Please try again.';
        updateRobotMessage('No speech detected');
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

  // Voice type selection
  voiceMaleBtn.addEventListener('click', function () {
    currentVoiceType = 'male';
    voiceMaleBtn.classList.add('active');
    voiceFemaleBtn.classList.remove('active');
  });

  voiceFemaleBtn.addEventListener('click', function () {
    currentVoiceType = 'female';
    voiceFemaleBtn.classList.add('active');
    voiceMaleBtn.classList.remove('active');
  });

  // Test voice button
  testVoiceBtn.addEventListener('click', function () {
    const t = translations[currentLanguage];
    speak(t.testMessage);
    updateRobotMessage(t.testMessage);
  });

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
    document.getElementById('allBlinkText').textContent = t.allBlink;

    // Update AI language indicator
    aiLanguage.textContent = lang === 'en-US' ? 'English' : 'Filipino';

    // Update DHT title
    const dhtTitle = document.getElementById('dhtTitle');
    if (dhtTitle) dhtTitle.textContent = t.dhtTitle;

    // Update voice selection text
    document.getElementById('voiceSelectTitle').textContent = t.voiceSelectTitle;
    document.getElementById('voiceMaleText').textContent = t.maleVoice;
    document.getElementById('voiceFemaleText').textContent = t.femaleVoice;
    document.getElementById('testVoiceText').textContent = t.testVoice;

    // Update robot text
    document.getElementById('robotTitle').textContent = t.robotTitle;
    updateRobotStatus(t.robotReady);
    robotStatusTagalog.textContent = translations['fil-PH'].robotReady;

    // Show/hide Tagalog labels
    document.querySelectorAll('.led-label-tagalog').forEach(el => {
      el.classList.toggle('hidden', lang !== 'fil-PH');
    });

    // Show/hide DHT Tagalog labels
    document.querySelectorAll('.dht-label-tagalog').forEach(el => {
      el.classList.toggle('hidden', lang !== 'fil-PH');
    });

    // Show/hide robot Tagalog status
    robotStatusTagalog.classList.toggle('hidden', lang !== 'fil-PH');

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
      const t = translations[currentLanguage];

      if (data.success) {
        const actionText = formatAction(data.action);
        commandStatus.textContent = `✓ Command executed: ${actionText}`;
        commandStatus.className = 'command-status success';
        updateLEDStates(data.states);
        updateRobotLEDs(data.states);

        // Speak confirmation
        const confirmMsg = currentLanguage === 'en-US'
          ? `${actionText} done!`
          : `${actionText} tapos na!`;
        speak(confirmMsg);
        updateRobotMessage(confirmMsg);
        updateRobotStatus(t.robotExecuted);

      } else if (data.invalid_color) {
        // Show notification for invalid color
        showNotification(data.message);
        commandStatus.textContent = `✗ ${data.message}`;
        commandStatus.className = 'command-status error';

        // Trigger buzzer animation
        buzzerIcon.classList.add('on');
        setTimeout(() => buzzerIcon.classList.remove('on'), 500);

        // Speak error
        const errorMsg = currentLanguage === 'en-US'
          ? `Sorry, ${data.color} LED is not available. Only white, blue, and red LEDs are available.`
          : `Pasensya, ang ${data.color} na LED ay hindi available. White, blue, at red LED lamang ang available.`;
        speak(errorMsg);
        updateRobotMessage(data.message);
        updateRobotStatus(t.robotError);

      } else {
        commandStatus.textContent = `✗ ${data.error || 'Command not recognized'}`;
        commandStatus.className = 'command-status error';

        // Speak error
        const errorMsg = currentLanguage === 'en-US'
          ? "Sorry, I didn't understand that command. Please try again."
          : "Pasensya, hindi ko naintindihan. Pakiulit.";
        speak(errorMsg);
        updateRobotMessage(errorMsg);
        updateRobotStatus(t.robotError);
      }

      if (data.states) {
        updateLEDStates(data.states);
        updateRobotLEDs(data.states);
      }
    } catch (error) {
      console.error('Error processing command:', error);
      commandStatus.textContent = '✗ Error processing command';
      commandStatus.className = 'command-status error';
    }
  }

  // Update robot LEDs (eyes and nose)
  function updateRobotLEDs(states) {
    // Left eye = Blue LED
    robotLeftEye.classList.toggle('on', states.blue);
    robotLeftEye.classList.toggle('blinking-led', states.blue_blink);

    // Right eye = Red LED
    robotRightEye.classList.toggle('on', states.red);
    robotRightEye.classList.toggle('blinking-led', states.red_blink);

    // Nose = White LED
    robotNose.classList.toggle('on', states.white);
    robotNose.classList.toggle('blinking', states.white_blink);
  }

  function formatAction(action) {
    const actionLabels = {
      'white_on': 'White LED ON',
      'white_off': 'White LED OFF',
      'white_blink': 'White LED Blinking',
      'blue_on': 'Blue LED ON',
      'blue_off': 'Blue LED OFF',
      'blue_blink': 'Blue LED Blinking',
      'red_on': 'Red LED ON',
      'red_off': 'Red LED OFF',
      'red_blink': 'Red LED Blinking',
      'all_on': 'All LEDs ON',
      'all_off': 'All LEDs OFF',
      'all_blink': 'All LEDs Blinking',
      'buzzer': 'Buzzer activated'
    };
    return actionLabels[action] || action;
  }

  // Update LED visual states
  function updateLEDStates(states) {
    // White LED
    whiteLedIcon.classList.toggle('on', states.white);
    whiteLedIcon.classList.toggle('blinking', states.white_blink);

    // Blue LED
    blueLedIcon.classList.toggle('on', states.blue);
    blueLedIcon.classList.toggle('blinking', states.blue_blink);

    // Red LED
    redLedIcon.classList.toggle('on', states.red);
    redLedIcon.classList.toggle('blinking', states.red_blink);

    if (states.buzzer) {
      buzzerIcon.classList.add('on');
      setTimeout(() => buzzerIcon.classList.remove('on'), 300);
    }

    // Also update robot LEDs
    updateRobotLEDs(states);
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

          // Update robot message
          const actionText = `${led.charAt(0).toUpperCase() + led.slice(1)} ${action.toUpperCase()}`;
          updateRobotMessage(actionText);
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

  // All Blink button
  document.getElementById('allBlinkBtn').addEventListener('click', async function () {
    try {
      const response = await fetch('/api/led/all/blink', { method: 'POST' });
      const data = await response.json();
      if (data.success) {
        updateLEDStates(data.states);
      }
    } catch (error) {
      console.error('Error:', error);
    }
  });

  // DHT11 Sensor Reading
  const temperatureValue = document.getElementById('temperatureValue');
  const humidityValue = document.getElementById('humidityValue');
  const dhtStatus = document.getElementById('dhtStatus');

  async function fetchDHTData() {
    try {
      const response = await fetch('/api/dht');
      const data = await response.json();
      const t = translations[currentLanguage];

      if (data.success) {
        const temp = data.temperature !== null ? data.temperature : '--';
        const hum = data.humidity !== null ? data.humidity : '--';

        temperatureValue.textContent = temp;
        humidityValue.textContent = hum;

        // Update robot ear displays
        robotTemp.textContent = temp;
        robotHumidity.textContent = hum;

        const now = new Date().toLocaleTimeString();
        dhtStatus.textContent = `${t.dhtUpdated} ${now}`;
        dhtStatus.className = 'dht-status success';
      } else {
        dhtStatus.textContent = t.dhtError;
        dhtStatus.className = 'dht-status error';
      }
    } catch (error) {
      console.error('Error fetching DHT data:', error);
      const t = translations[currentLanguage];
      dhtStatus.textContent = t.dhtError;
      dhtStatus.className = 'dht-status error';
    }
  }

  // Fetch DHT data every 3 seconds
  fetchDHTData();
  setInterval(fetchDHTData, 3000);

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
        updateRobotLEDs(data.states);
      }
    } catch (error) {
      console.error('Error fetching initial state:', error);
    }
  }

  fetchInitialState();

  // Welcome message on load
  setTimeout(() => {
    const t = translations[currentLanguage];
    updateRobotMessage(t.robotReady);
  }, 500);
});
