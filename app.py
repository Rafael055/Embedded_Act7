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

# Voice command mappings for English and Tagalog
COMMANDS = {
    'en-US': {
        'white_on': ['turn on white', 'white on', 'white led on', 'turn white on', 'turn on the white', 'turn on white led'],
        'white_off': ['turn off white', 'white off', 'white led off', 'turn white off', 'turn off the white', 'turn off white led'],
        'blue_on': ['turn on blue', 'blue on', 'blue led on', 'turn blue on', 'turn on the blue', 'turn on blue led'],
        'blue_off': ['turn off blue', 'blue off', 'blue led off', 'turn blue off', 'turn off the blue', 'turn off blue led'],
        'red_on': ['turn on red', 'red on', 'red led on', 'turn red on', 'turn on the red', 'turn on red led'],
        'red_off': ['turn off red', 'red off', 'red led off', 'turn red off', 'turn off the red', 'turn off red led'],
        'all_on': ['turn on all', 'all on', 'all lights on', 'turn all on', 'turn on all lights'],
        'all_off': ['turn off all', 'all off', 'all lights off', 'turn all off', 'turn off all lights'],
        'white_blink': ['blink white', 'white blink', 'blink white led', 'flash white', 'white flash'],
        'blue_blink': ['blink blue', 'blue blink', 'blink blue led', 'flash blue', 'blue flash'],
        'red_blink': ['blink red', 'red blink', 'blink red led', 'flash red', 'red flash'],
        'all_blink': ['blink all', 'all blink', 'blink all lights', 'flash all', 'all flash'],
        'buzzer': ['buzzer', 'buzz', 'beep', 'sound'],
        # Color keywords for detection
        'valid_colors': ['white', 'blue', 'red'],
        'invalid_color_keywords': ['green', 'yellow', 'orange', 'purple', 'pink', 'black', 'brown', 'grey', 'gray', 'violet', 'cyan', 'magenta']
    },
    'fil-PH': {
        'white_on': ['buksan ang puting LED', 'puting ilaw i-bukas', 'i on puting ilaw', 'buksan ang puting ilaw'],
        'white_off': ['patayin ang puting LED', 'puting ilaw patayin', 'i off puting ilaw', 'patayin ang puting ilaw', 'puting ilaw patayin'],
        'blue_on': ['buksan ang asul na ilaw', 'asul na ilaw i-bukas', 'i on asul na ilaw', 'buksan ang asul na ilaw', 'asul na ilaw i-bukas'],
        'blue_off': ['patayin ang asul na ilaw', 'asul na ilaw patayin', 'i off asul na ilaw', 'patayin ang asul na ilaw', 'asul na ilaw patay'],
        'red_on': ['buksan ang pulang ilaw', 'pulang ilaw i-bukas', 'i on pulang ilaw', 'buksan ang pulang ilaw', 'pulang ilaw i-bukas'],
        'red_off': ['patayin ang pulang ilaw', 'pulang ilaw patayin', 'i off pulang ilaw', 'patayin ang pulang ilaw', 'pulang ilaw patay'],
        'all_on': ['buksan ang lahat ng ilaw', 'lahat bukas', 'i on lahat', 'buksan ang lahat ng ilaw'],
        'all_off': ['patayin ang lahat ng ilaw', 'lahat ng ilaw patayin', 'i-off lahat', 'i-off lahat ng ilaw'],
        'white_blink': ['kumukurap na puting  ilaw', 'i blink ang puting ilaw', 'pakurap-kurap na puting ilaw', 'puting ilaw na kumukurap'],
        'blue_blink': ['kumukurap na asul  ilaw', 'i blink ang asul na ilaw', 'pakurap-kurap na asul na ilaw', 'asul na ilaw na kumukurap'],
        'red_blink': ['kumukurap na pulang ilaw', 'i blink ang pulang ilaw', 'pakurap-kurap na pulang ilaw', 'pulang ilaw na kumukurap'],
        'all_blink': ['kumukurap ang lahat ng ilaw', 'i blink lahat', 'pakurap-kurap ang lahat ng ilaw', 'lahat ay kumukurap'],
        'buzzer': ['buzzer', 'tunog', 'beep'],
        'valid_colors': ['puti', 'asul', 'pula'],
        'invalid_color_keywords': ['berde', 'dilaw', 'orange', 'lila', 'rosas', 'itim', 'kayumanggi', 'abo', 'violet']
    }
}

def process_voice_command(text, language):
    """Process voice command and return action"""
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
    
    if action == 'white_on':
        led_controller.turn_on_white()
    elif action == 'white_off':
        led_controller.turn_off_white()
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
    elif action == 'white_blink':
        led_controller.blink_white()
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
        if led_name == 'white':
            if action == 'on':
                led_controller.turn_on_white()
            elif action == 'blink':
                led_controller.blink_white()
            else:
                led_controller.turn_off_white()
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
        return jsonify({'success': False, 'error': 'No text provided'})
    
    # Process the command
    command_result = process_voice_command(text, language)
    
    if command_result['invalid_color']:
        # Trigger buzzer for invalid color
        led_controller.buzz(0.5)
        return jsonify({
            'success': False,
            'invalid_color': True,
            'color': command_result.get('color', 'unknown'),
            'message': f"Invalid color: {command_result.get('color', 'unknown')}. Only White, Blue, and Red LEDs are available!",
            'states': led_controller.get_states()
        })
    
    if command_result['success']:
        exec_result = execute_command(command_result['action'])
        return jsonify({
            'success': True,
            'action': command_result['action'],
            'states': exec_result['states']
        })
    
    return jsonify({
        'success': False,
        'error': 'Command not recognized',
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
