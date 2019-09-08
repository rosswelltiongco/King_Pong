gpio_pin = 8
INDEFINITE = 999

class Fan:
    def __init__(self,gpio_pin):
        """
        Initialize code
        """
        self.fan_pin = gpio_pin

    def get_pin(self):
        """
        Returns: Gpio pin
        """
        return self.fan_pin

    def start_fan(self,pwm_value):
        """
        Args:
            pwm_value (int): value to run at
        
        Runs indefinitely
        """
        print("fan is running at {}".format(pwm_value))
        print(INDEFINITE)

    def stop_fan(self):
        """
        Terminates fan
        """
        print("fan stopped")
