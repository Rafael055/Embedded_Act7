# Act7 Virtual Environment Setup

## Running the Application

The virtual environment is already set up and configured. Use one of these methods:

### Method 1: Using the run script (Recommended)
```bash
cd /home/pi/Documents/Embedded/act7
./run.sh
```

### Method 2: Manual activation
```bash
cd /home/pi/Documents/Embedded/act7
source .venv/bin/activate
export PYTHONPATH="/usr/lib/python3/dist-packages:$PYTHONPATH"
python app.py
```

### Method 3: Direct command
```bash
cd /home/pi/Documents/Embedded/act7
source .venv/bin/activate && PYTHONPATH="/usr/lib/python3/dist-packages:$PYTHONPATH" python app.py
```

## Installed Packages

The virtual environment includes:
- Flask (web framework)
- SpeechRecognition (voice recognition)
- gpiozero (GPIO control)
- lgpio (low-level GPIO)
- adafruit-circuitpython-dht (DHT sensor support)
- RPi.GPIO (Raspberry Pi GPIO)
- pyaudio (audio support - from system packages)

## Notes

- PyAudio is accessed from system packages due to compilation issues
- The `run.sh` script handles all necessary environment setup automatically
- ALSA warnings during startup are normal and can be ignored
