import time

import RPi.GPIO as GPIO

SENSOR_PIN = 4  # GPIO pin 4

GPIO.setmode(GPIO.BCM)  # broadcom pin numbering
GPIO.setup(SENSOR_PIN, GPIO.OUT)

# calibration data for charge times (in seconds)
MIN_CHARGE_TIME = 1.07e-9  # minimum charge time corresponds to maximum pressure (2 kg)
MAX_CHARGE_TIME = (
    0.35  # maximum charge time corresponds to minimum pressure (no pressure)
)


def discharge():
    """
    Discharges the sensor pin by setting it to LOW for a short period of time.
    """
    GPIO.setup(SENSOR_PIN, GPIO.OUT)
    GPIO.output(SENSOR_PIN, GPIO.LOW)
    time.sleep(0.5)


def charge_time():
    """
    Calculates the charge time of a sensor connected to a GPIO pin.

    Returns:
        float: The charge time in seconds.
    """
    GPIO.setup(SENSOR_PIN, GPIO.IN)
    start_time = time.time()
    while GPIO.input(SENSOR_PIN) == GPIO.LOW:
        pass
    return time.time() - start_time


def calculate_pressure_percentage(charge):
    """
    Calculates the pressure percentage based on the charge time.

    Args:
        charge (float): The charge time in seconds.

    Returns:
        float: The pressure percentage, ranging from 0 to 100.
    """
    if charge <= MIN_CHARGE_TIME:
        return 100  # Maximum pressure
    elif charge >= MAX_CHARGE_TIME:
        return 0  # Minimum pressure
    else:
        # Calculate percentage from the inverted range
        return 100 - (
            (charge - MIN_CHARGE_TIME) / (MAX_CHARGE_TIME - MIN_CHARGE_TIME) * 100
        )


try:
    while True:
        discharge()
        charge = charge_time()
        pressure_percentage = calculate_pressure_percentage(charge)
        print(f"Pressure: {pressure_percentage:.2f}%")
        time.sleep(1)

except KeyboardInterrupt:
    GPIO.cleanup()  # clean up GPIO to reset the pin configuration
