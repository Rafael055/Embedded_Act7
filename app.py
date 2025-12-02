from flask import Flask, render_template, jsonify, request
import threading
import time
import speech_recognition as sr
from Leds import LEDController

app = Flask(__name__)

# Initialize LED controller
led_controller = LEDController()

# Voice recognition settings
recognizer = sr.Recognizer()
microphone = sr.Microphone()

# Current language setting (default: English)
current_language = 'en-US'

# Voice command mappings
COMMANDS = {
    'en-US': {
        'green_on': ['turn on green', 'green on', 'switch on green'],
        'green_off': ['turn off green', 'green off', 'switch off green'],
        'blue_on': ['turn on blue', 'blue on', 'switch on blue'],
        'blue_off': ['turn off blue', 'blue off', 'switch off blue'],
        'red_on': ['turn on red', 'red on', 'switch on red'],
        'red_off': ['turn off red', 'red off', 'switch off red'],
        'all_on': ['turn on all', 'all on', 'turn on all', 'all lights on'],
        'all_off': ['turn off all', 'all off', 'switch off all', 'all lights off'],
        'green_blink': ['blink green', 'flash green'],
        'blue_blink': ['blink blue', 'flash blue'],
        'red_blink': ['blink red', 'flash red'],
        'all_blink': ['blink all', 'flash all'],
        'buzzer': ['buzzer', 'buzz', 'beep'],
        'invalid_color_keywords': ['white', 'yellow', 'orange', 'purple', 'pink', 'black', 'brown', 'grey', 'gray', 'violet', 'cyan', 'magenta']
    },
    'fil-PH': {
        'green_on': ['buksan ang berdeng ilaw', 'i on berdeng ilaw'],
        'green_off': ['patayin ang berdeng ilaw', 'i off berdeng ilaw'],
        'blue_on': ['buksan ang asul na ilaw', 'i on asul na ilaw'],
        'blue_off': ['patayin ang asul na ilaw', 'i off asul na ilaw'],
        'red_on': ['buksan ang pulang ilaw', 'i on pulang ilaw'],
        'red_off': ['patayin ang pulang ilaw', 'i off pulang ilaw'],
        'all_on': ['buksan ang lahat ng ilaw', 'i on lahat'],
        'all_off': ['patayin ang lahat ng ilaw', 'i off lahat'],
        'green_blink': ['i blink ang berdeng ilaw', 'pakurap berdeng ilaw'],
        'blue_blink': ['i blink ang asul na ilaw', 'pakurap asul na ilaw'],
        'red_blink': ['i blink ang pulang ilaw', 'pakurap pulang ilaw'],
        'all_blink': ['i blink lahat', 'pakurap lahat'],
        'buzzer': ['buzzer', 'tunog', 'beep'],
        'invalid_color_keywords': ['puti', 'dilaw', 'orange', 'lila', 'rosas', 'itim', 'kayumanggi', 'abo', 'violet']
    }
}

def process_voice_command(text, language):
    """Process voice command using hardcoded patterns"""
    text = text.lower().strip()
    commands = COMMANDS.get(language, COMMANDS['en-US'])
    
    # Check for valid LED commands
    for action, phrases in commands.items():
        if action in ['valid_colors', 'invalid_color_keywords']:
            continue
        for phrase in phrases:
            if phrase in text:
                return {'action': action, 'success': True, 'invalid_color': False}
    
    # Check if user mentioned an invalid color
    for invalid_color in commands.get('invalid_color_keywords', []):
        if invalid_color in text:
            return {'action': 'invalid_color', 'success': False, 'invalid_color': True, 'color': invalid_color}
    
    return {'action': 'unknown', 'success': False, 'invalid_color': False}

def execute_command(action):
    """Execute the LED/buzzer command"""
    result = {'success': True, 'states': {}} 

    if action == 'green_on':
        led_controller.turn_on_green()
    elif action == 'green_off':
        led_controller.turn_off_green()
    elif action == 'blue_on':
        led_controller.turn_on_blue()
    elif action == 'blue_off':
        led_controller.turn_off_blue()
    elif action == 'red_on':
        led_controller.turn_on_red()
    elif action == 'red_off':
        led_controller.turn_off_red()
    elif action == 'all_on':
        led_controller.all_on()
    elif action == 'all_off':
        led_controller.all_off()
    elif action == 'green_blink':
        led_controller.blink_green()
    elif action == 'blue_blink':
        led_controller.blink_blue()
    elif action == 'red_blink':
        led_controller.blink_red()
    elif action == 'all_blink':
        led_controller.blink_all()
    elif action == 'buzzer':
        led_controller.buzz(0.3)
    else:
        result['success'] = False
    
    result['states'] = led_controller.get_states()
    return result

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/led/<led_name>/<action>', methods=['POST'])
def control_led(led_name, action):
    """Control LED via button click"""
    try:
        if led_name == 'green':
            if action == 'on':
                led_controller.turn_on_green()
            elif action == 'blink':
                led_controller.blink_green()
            else:
                led_controller.turn_off_green()
        elif led_name == 'blue':
            if action == 'on':
                led_controller.turn_on_blue()
            elif action == 'blink':
                led_controller.blink_blue()
            else:
                led_controller.turn_off_blue()
        elif led_name == 'red':
            if action == 'on':
                led_controller.turn_on_red()
            elif action == 'blink':
                led_controller.blink_red()
            else:
                led_controller.turn_off_red()
        elif led_name == 'buzzer':
            led_controller.buzz(0.3)
        elif led_name == 'all':
            if action == 'on':
                led_controller.all_on()
            elif action == 'blink':
                led_controller.blink_all()
            else:
                led_controller.all_off()
        
        return jsonify({
            'success': True,
            'states': led_controller.get_states()
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/states', methods=['GET'])
def get_states():
    """Get current LED states"""
    return jsonify({
        'success': True,
        'states': led_controller.get_states()
    })

@app.route('/api/dht', methods=['GET'])
def get_dht():
    """Get DHT11 temperature and humidity reading"""
    reading = led_controller.get_dht_reading()
    return jsonify(reading)

@app.route('/api/set_language', methods=['POST'])
def set_language():
    """Set voice recognition language"""
    global current_language
    data = request.get_json()
    language = data.get('language', 'en-US')
    
    if language in ['en-US', 'fil-PH']:
        current_language = language
        return jsonify({'success': True, 'language': current_language})
    
    return jsonify({'success': False, 'error': 'Invalid language'})

@app.route('/api/get_language', methods=['GET'])
def get_language():
    """Get current language"""
    return jsonify({'success': True, 'language': current_language})

@app.route('/api/voice_command', methods=['POST'])
def voice_command():
    """Process voice command from browser Web Speech API"""
    global current_language
    data = request.get_json()
    text = data.get('text', '')
    language = data.get('language', current_language)
    
    if not text:
        return jsonify({'success': False, 'error': 'No text provided', 'invalid_color': False})
    
    # Process the command
    command_result = process_voice_command(text, language)
    
    # Ensure invalid_color field exists
    if 'invalid_color' not in command_result:
        command_result['invalid_color'] = False
    
    if command_result.get('invalid_color', False):
        # Trigger buzzer for invalid color
        led_controller.buzz(0.5)
        return jsonify({
            'success': False,
            'invalid_color': True,
            'color': command_result.get('color', 'unknown'),
            'message': f"Invalid color: {command_result.get('color', 'unknown')}. Only White, Blue, and Red LEDs are available!",
            'states': led_controller.get_states()
        })
    
    if command_result.get('success', False):
        exec_result = execute_command(command_result['action'])
        return jsonify({
            'success': True,
            'action': command_result['action'],
            'invalid_color': False,
            'states': exec_result['states']
        })
    
    return jsonify({
        'success': False,
        'error': 'Command not recognized',
        'invalid_color': False,
        'text': text,
        'states': led_controller.get_states()
    })

@app.route('/api/listen', methods=['POST'])
def listen_voice():
    """Listen for voice command using server-side speech recognition (backup)"""
    global current_language
    data = request.get_json() or {}
    language = data.get('language', current_language)
    
    try:
        with microphone as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        
        # Recognize speech
        text = recognizer.recognize_google(audio, language=language)
        print(f"Recognized: {text}")
        
        # Process command
        command_result = process_voice_command(text, language)
        
        if command_result['invalid_color']:
            led_controller.buzz(0.5)
            return jsonify({
                'success': False,
                'invalid_color': True,
                'color': command_result.get('color', 'unknown'),
                'message': f"Invalid color: {command_result.get('color', 'unknown')}. Only White, Blue, and Red LEDs are available!",
                'text': text,
                'states': led_controller.get_states()
            })
        
        if command_result['success']:
            exec_result = execute_command(command_result['action'])
            return jsonify({
                'success': True,
                'action': command_result['action'],
                'text': text,
                'states': exec_result['states']
            })
        
        return jsonify({
            'success': False,
            'error': 'Command not recognized',
            'text': text,
            'states': led_controller.get_states()
        })
        
    except sr.WaitTimeoutError:
        return jsonify({'success': False, 'error': 'No speech detected. Please try again.'})
    except sr.UnknownValueError:
        return jsonify({'success': False, 'error': 'Could not understand audio. Please try again.'})
    except sr.RequestError as e:
        return jsonify({'success': False, 'error': f'Speech service error: {str(e)}'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def cleanup():
    """Cleanup GPIO on exit"""
    led_controller.cleanup()

import atexit
atexit.register(cleanup)

if __name__ == '__main__':
    print("Starting Voice-Controlled LED Server...")
    print("Access the web interface at http://<your-pi-ip>:5000")
    # Use use_reloader=False to prevent GPIO conflicts on restart
    app.run(host='0.0.0.0', port=5000, debug=True, threaded=True, use_reloader=False)
