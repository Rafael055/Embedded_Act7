from gpiozero import LED, Buzzer as GpioZeroBuzzer
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
import time
import adafruit_dht
import board

# Set the pin factory to lgpio for Raspberry Pi 5 / newer OS
Device.pin_factory = LGPIOFactory()

# Raspberry Pi Physical Pin Numbers (Board mode) -> BCM GPIO mapping
# Buzzer - Pin 11 -> GPIO 17
# Green LED - Pin 40 -> GPIO 21
# Blue LED - Pin 38 -> GPIO 20
# Red LED - Pin 36 -> GPIO 16
# DHT11 - Pin 32 -> GPIO 12

class LEDController:
    def __init__(self):
        # BCM GPIO numbers
        self.BUZZER_GPIO = 17   # Physical Pin 11
        self.GREEN_GPIO = 21    # Physical Pin 40
        self.BLUE_GPIO = 20     # Physical Pin 38
        self.RED_GPIO = 16      # Physical Pin 36
        self.DHT_GPIO = 12      # Physical Pin 32
        
        # Initialize components using gpiozero
        self.green_led = LED(self.GREEN_GPIO)
        self.blue_led = LED(self.BLUE_GPIO)
        self.red_led = LED(self.RED_GPIO)
        self.buzzer = GpioZeroBuzzer(self.BUZZER_GPIO)
        
        # Initialize DHT11 sensor
        self.dht_sensor = adafruit_dht.DHT11(board.D12)
        
        # Initial state - all off
        self.led_states = {
            'green': False,
            'blue': False,
            'red': False,
            'buzzer': False,
            'green_blink': False,
            'blue_blink': False,
            'red_blink': False
        }
        
        # Blinking threads
        self.blink_threads = {}
        self.stop_blink_flags = {}
        
        # Turn all off initially
        self.all_off()
    
    def turn_on_green(self):
        self.stop_blink_flags['green'] = True
        self.green_led.on()
        self.led_states['green'] = True
        self.led_states['green_blink'] = False
        
    def turn_off_green(self):
        self.stop_blink_flags['green'] = True
        self.green_led.off()
        self.led_states['green'] = False
        self.led_states['green_blink'] = False
    
    def turn_on_blue(self):
        self.stop_blink_flags['blue'] = True
        self.blue_led.on()
        self.led_states['blue'] = True
        self.led_states['blue_blink'] = False
    
    def turn_off_blue(self):
        self.stop_blink_flags['blue'] = True
        self.blue_led.off()
        self.led_states['blue'] = False
        self.led_states['blue_blink'] = False
    
    def turn_on_red(self):
        self.stop_blink_flags['red'] = True
        self.red_led.on()
        self.led_states['red'] = True
        self.led_states['red_blink'] = False
    
    def turn_off_red(self):
        self.stop_blink_flags['red'] = True
        self.red_led.off()
        self.led_states['red'] = False
        self.led_states['red_blink'] = False
    
    def toggle_green(self):
        if self.led_states['green']:
            self.turn_off_green()
        else:
            self.turn_on_green()
        return self.led_states['green']
    
    def toggle_blue(self):
        if self.led_states['blue']:
            self.turn_off_blue()
        else:
            self.turn_on_blue()
        return self.led_states['blue']
    
    def toggle_red(self):
        if self.led_states['red']:
            self.turn_off_red()
        else:
            self.turn_on_red()
        return self.led_states['red']
    
    def buzz(self, duration=0.5):
        """Trigger buzzer for a short duration"""
        self.buzzer.on()
        self.led_states['buzzer'] = True
        time.sleep(duration)
        self.buzzer.off()
        self.led_states['buzzer'] = False
    
    def buzzer_on(self):
        self.buzzer.on()
        self.led_states['buzzer'] = True
        
    def buzzer_off(self):
        self.buzzer.off()
        self.led_states['buzzer'] = False
    
    def _blink_continuous(self, led, color, interval=0.5):
        """Continuous blinking in a thread"""
        while not self.stop_blink_flags.get(color, False):
            led.on()
            time.sleep(interval)
            led.off()
            time.sleep(interval)
    
    def blink_green(self, times=None, interval=0.5):
        """Blink green LED - continuous if times=None"""
        import threading
        
        # Stop any existing blink
        self.stop_blink_flags['green'] = True
        if 'green' in self.blink_threads:
            self.blink_threads['green'].join(timeout=1)
        
        if times is None:
            # Continuous blinking
            self.stop_blink_flags['green'] = False
            thread = threading.Thread(target=self._blink_continuous, args=(self.green_led, 'green', interval))
            thread.daemon = True
            thread.start()
            self.blink_threads['green'] = thread
            self.led_states['green'] = False
            self.led_states['green_blink'] = True
        else:
            # Fixed number of blinks
            for _ in range(times):
                self.green_led.on()
                time.sleep(interval)
                self.green_led.off()
                time.sleep(interval)
            self.led_states['green'] = False
            self.led_states['green_blink'] = False
    
    def blink_blue(self, times=None, interval=0.5):
        """Blink blue LED - continuous if times=None"""
        import threading
        
        # Stop any existing blink
        self.stop_blink_flags['blue'] = True
        if 'blue' in self.blink_threads:
            self.blink_threads['blue'].join(timeout=1)
        
        if times is None:
            # Continuous blinking
            self.stop_blink_flags['blue'] = False
            thread = threading.Thread(target=self._blink_continuous, args=(self.blue_led, 'blue', interval))
            thread.daemon = True
            thread.start()
            self.blink_threads['blue'] = thread
            self.led_states['blue'] = False
            self.led_states['blue_blink'] = True
        else:
            # Fixed number of blinks
            for _ in range(times):
                self.blue_led.on()
                time.sleep(interval)
                self.blue_led.off()
                time.sleep(interval)
            self.led_states['blue'] = False
            self.led_states['blue_blink'] = False
    
    def blink_red(self, times=None, interval=0.5):
        """Blink red LED - continuous if times=None"""
        import threading
        
        # Stop any existing blink
        self.stop_blink_flags['red'] = True
        if 'red' in self.blink_threads:
            self.blink_threads['red'].join(timeout=1)
        
        if times is None:
            # Continuous blinking
            self.stop_blink_flags['red'] = False
            thread = threading.Thread(target=self._blink_continuous, args=(self.red_led, 'red', interval))
            thread.daemon = True
            thread.start()
            self.blink_threads['red'] = thread
            self.led_states['red'] = False
            self.led_states['red_blink'] = True
        else:
            # Fixed number of blinks
            for _ in range(times):
                self.red_led.on()
                time.sleep(interval)
                self.red_led.off()
                time.sleep(interval)
            self.led_states['red'] = False
            self.led_states['red_blink'] = False
    
    def blink_all(self, times=None, interval=0.5):
        """Blink all LEDs"""
        if times is None:
            # Start all continuous blinking
            self.blink_green(times=None, interval=interval)
            self.blink_blue(times=None, interval=interval)
            self.blink_red(times=None, interval=interval)
        else:
            # Fixed number of blinks
            for _ in range(times):
                self.green_led.on()
                self.blue_led.on()
                self.red_led.on()
                time.sleep(interval)
                self.green_led.off()
                self.blue_led.off()
                self.red_led.off()
                time.sleep(interval)
            self.led_states['green'] = False
            self.led_states['blue'] = False
            self.led_states['red'] = False
            self.led_states['green_blink'] = False
            self.led_states['blue_blink'] = False
            self.led_states['red_blink'] = False
    
    def all_off(self):
        # Stop all blinking
        for color in ['green', 'blue', 'red']:
            self.stop_blink_flags[color] = True
        
        self.green_led.off()
        self.blue_led.off()
        self.red_led.off()
        self.buzzer.off()
        self.led_states = {
            'green': False,
            'blue': False,
            'red': False,
            'buzzer': False,
            'green_blink': False,
            'blue_blink': False,
            'red_blink': False
        }
    
    def all_on(self):
        # Stop all blinking
        for color in ['green', 'blue', 'red']:
            self.stop_blink_flags[color] = True
        
        self.green_led.on()
        self.blue_led.on()
        self.red_led.on()
        self.led_states['green'] = True
        self.led_states['blue'] = True
        self.led_states['red'] = True
        self.led_states['green_blink'] = False
        self.led_states['blue_blink'] = False
        self.led_states['red_blink'] = False
    
    def get_states(self):
        return self.led_states
    
    def get_dht_reading(self):
        """Read temperature and humidity from DHT11 sensor"""
        try:
            temperature = self.dht_sensor.temperature
            humidity = self.dht_sensor.humidity
            return {
                'success': True,
                'temperature': temperature,
                'humidity': humidity
            }
        except RuntimeError as e:
            # DHT sensors can occasionally fail to read
            return {
                'success': False,
                'error': str(e)
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def cleanup(self):
        self.all_off()
        self.green_led.close()
        self.blue_led.close()
        self.red_led.close()
        self.buzzer.close()
        self.dht_sensor.exit()


# For testing
if __name__ == "__main__":
    controller = LEDController()
    
    print("Testing LEDs...")
    
    print("Green LED ON")
    controller.turn_on_green()
    time.sleep(1)
    
    print("Blue LED ON")
    controller.turn_on_blue()
    time.sleep(1)
    
    print("Red LED ON")
    controller.turn_on_red()
    time.sleep(1)
    
    print("Buzzer test")
    controller.buzz(5)
    
    print("All OFF")
    controller.all_off()
    time.sleep(1)
    
    controller.cleanup()
    print("Test complete!")
