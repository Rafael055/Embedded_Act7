from gpiozero import LED, Buzzer as GpioZeroBuzzer
from gpiozero.pins.lgpio import LGPIOFactory
from gpiozero import Device
import time

# Set the pin factory to lgpio for Raspberry Pi 5 / newer OS
Device.pin_factory = LGPIOFactory()

# Raspberry Pi Physical Pin Numbers (Board mode) -> BCM GPIO mapping
# Buzzer - Pin 11 -> GPIO 17
# White LED - Pin 40 -> GPIO 21
# Blue LED - Pin 38 -> GPIO 20
# Red LED - Pin 36 -> GPIO 16

class LEDController:
    def __init__(self):
        # BCM GPIO numbers
        self.BUZZER_GPIO = 17   # Physical Pin 11
        self.WHITE_GPIO = 21    # Physical Pin 40
        self.BLUE_GPIO = 20     # Physical Pin 38
        self.RED_GPIO = 16      # Physical Pin 36
        
        # Initialize components using gpiozero
        self.white_led = LED(self.WHITE_GPIO)
        self.blue_led = LED(self.BLUE_GPIO)
        self.red_led = LED(self.RED_GPIO)
        self.buzzer = GpioZeroBuzzer(self.BUZZER_GPIO)
        
        # Initial state - all off
        self.led_states = {
            'white': False,
            'blue': False,
            'red': False,
            'buzzer': False
        }
        
        # Turn all off initially
        self.all_off()
    
    def turn_on_white(self):
        self.white_led.on()
        self.led_states['white'] = True
        
    def turn_off_white(self):
        self.white_led.off()
        self.led_states['white'] = False
        
    def turn_on_blue(self):
        self.blue_led.on()
        self.led_states['blue'] = True
        
    def turn_off_blue(self):
        self.blue_led.off()
        self.led_states['blue'] = False
        
    def turn_on_red(self):
        self.red_led.on()
        self.led_states['red'] = True
        
    def turn_off_red(self):
        self.red_led.off()
        self.led_states['red'] = False
    
    def toggle_white(self):
        if self.led_states['white']:
            self.turn_off_white()
        else:
            self.turn_on_white()
        return self.led_states['white']
    
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
    
    def all_off(self):
        self.white_led.off()
        self.blue_led.off()
        self.red_led.off()
        self.buzzer.off()
        self.led_states = {
            'white': False,
            'blue': False,
            'red': False,
            'buzzer': False
        }
    
    def all_on(self):
        self.white_led.on()
        self.blue_led.on()
        self.red_led.on()
        self.led_states['white'] = True
        self.led_states['blue'] = True
        self.led_states['red'] = True
    
    def get_states(self):
        return self.led_states
    
    def cleanup(self):
        self.all_off()
        self.white_led.close()
        self.blue_led.close()
        self.red_led.close()
        self.buzzer.close()


# For testing
if __name__ == "__main__":
    controller = LEDController()
    
    print("Testing LEDs...")
    
    print("White LED ON")
    controller.turn_on_white()
    time.sleep(1)
    
    print("Blue LED ON")
    controller.turn_on_blue()
    time.sleep(1)
    
    print("Red LED ON")
    controller.turn_on_red()
    time.sleep(1)
    
    print("Buzzer test")
    controller.buzz(0.3)
    
    print("All OFF")
    controller.all_off()
    time.sleep(1)
    
    controller.cleanup()
    print("Test complete!")
