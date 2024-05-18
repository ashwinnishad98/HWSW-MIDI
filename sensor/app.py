import math
import time

import firebase_admin
import pygame
import RPi.GPIO as GPIO
import spidev
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("firebasepvt.json")
firebase_admin.initialize_app(
    cred, {"databaseURL": "https://hwsw2-e6856-default-rtdb.firebaseio.com/"}
)

# Initialize pygame mixer
pygame.init()
pygame.mixer.init()
drum_sound = pygame.mixer.Sound("kick1.wav")
drum_intensity_sound = pygame.mixer.Sound("kick1.wav")

# Setup SPI for MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1350000

# Setup GPIO for LED
led_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(led_pin, GPIO.OUT)

pwm = GPIO.PWM(led_pin, 1000)  # Set PWM frequency to 1000 Hz
pwm.start(0)  # Start PWM with 0% duty cycle

# Define timing for the notes
note_times = [1, 2, 3, 5, 7]
tolerance = 0.5

numReadings = 10  # Number of readings to average
readings = [0] * numReadings  # Initialize readings array
readIndex = 0  # Index for the current reading
total = 0  # Total sum of the readings
average = 0  # Average of the readings


def update_leaderboard(username, score):
    ref = db.reference("leaderboard")
    user_ref = ref.child(username)
    user_data = user_ref.get()
    if user_data is None:
        user_ref.set({"username": username, "score": score})
    else:
        current_score = user_data["score"]
        if score > current_score:
            user_ref.update({"score": score})


def read_channel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data


def update_average(new_value):
    """
    Updates the average value based on a new reading.

    Args:
        new_value (float): The new reading to be added to the average calculation.

    Returns:
        float: The updated average value.

    """
    global total, readIndex, readings, average
    total -= readings[readIndex]  # Subtract the oldest reading from the total
    readings[readIndex] = new_value  # Add the new reading to the array
    total += readings[readIndex]  # Add the new reading to the total
    readIndex = (
        readIndex + 1
    ) % numReadings  # Advance to the next position in the array
    average = total / numReadings  # Calculate the average
    return average


def map_value(x, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another range.

    Returns:
    float: The mapped value.

    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


def play_sequence():
    """
    Plays a sequence of notes with corresponding LED lights.

    This function iterates over the `note_times` list and plays a drum sound
    while lighting up an LED for each note. The LED remains on for a duration
    of 0.1 seconds.

    Args:
        None

    Returns:
        None
    """
    start_time = time.time()
    for note_time in note_times:
        while time.time() < start_time + note_time:
            time.sleep(0.01)
        GPIO.output(led_pin, True)
        drum_sound.play()  # Play the drum sound when LED lights up
        time.sleep(0.1)  # LED on duration
        GPIO.output(led_pin, False)


def record_responses():
    start_time = time.time()
    scores = []
    response_times = []
    last_second = 0

    while time.time() - start_time < 10:
        current_time = time.time() - start_time
        current_second = int(current_time)

        if current_second != last_second:  # Print every new second
            print(f"{current_second} second(s)")
            last_second = current_second

        sensor_value = read_channel(0)

        if sensor_value > 800:  # Threshold for sensor press
            response_times.append(current_time)
            GPIO.output(led_pin, True)
            drum_sound.play()  # Play the drum sound on sensor press
            time.sleep(0.1)  # LED feedback on sensor press
            GPIO.output(led_pin, False)
            while read_channel(0) > 800:  # Debounce by waiting for release
                time.sleep(0.01)

    # Check each response time against the expected times
    for note_time in note_times:
        scores.append(any(abs(note_time - t) <= tolerance for t in response_times))

    return scores


def lesson_rhythm():
    username = input("Enter your username to start the rhythm lesson: ")
    print("Lesson 1: Rhythm. Follow the LED and press on time.")
    input("Press Enter when ready to start...")
    print("Starting in 3 seconds...")
    time.sleep(1)
    print("2 seconds...")
    time.sleep(1)
    print("1 second...")
    time.sleep(1)
    play_sequence()
    print("Now, follow the sequence. Press on the seconds indicated starting in 3 seconds...")
    time.sleep(1)
    print("2 seconds...")
    time.sleep(1)
    print("1 second...")
    time.sleep(1)
    print("Start!")
    scores = record_responses()
    score = sum(scores)
    print(f"Your score: {score}/{len(note_times)}")
    update_leaderboard(username, score)


def lesson_intensity():
    print(
        "Lesson 2: Intensity. The volume and brightness will vary based on how hard you press the piezo sensor."
    )
    input("Press Enter when ready to start experimenting...")
    print(
        "Hit the piezo sensor with different intensities to test changes. Press CTRL+C to exit."
    )
    try:
        while True:
            sensor_value = read_channel(0)
            avg_sensor_value = update_average(sensor_value)  # Update the moving average
            exp_average = math.exp(
                avg_sensor_value / 1023 * 10
            )  # Scale and exponentiate
            brightness = map_value(
                exp_average, 1, math.exp(10), 0, 100
            )  # Map to PWM duty cycle

            pwm.ChangeDutyCycle(brightness)  # Adjust LED brightness
            if avg_sensor_value > 100:  # Threshold for sensor activation
                normalized_value = (
                    avg_sensor_value / 1023
                )  # Normalize the average sensor value to a 0.0-1.0 range
                drum_intensity_sound.set_volume(normalized_value)
                drum_intensity_sound.play()
                print(
                    f"Sensor Value: {sensor_value} | Moving Average: {avg_sensor_value} | LED Brightness: {brightness}%"
                )
            time.sleep(0.1)  # Time delay to avoid sound overlap
    except KeyboardInterrupt:
        pass
    finally:
        pwm.stop()


def main():
    while True:
        print("\nMenu:")
        print("1. Lesson 1: Rhythm")
        print("2. Lesson 2: Intensity")
        choice = input("Enter 1 or 2 to select a lesson, or 'exit' to quit: ")
        if choice == "1":
            lesson_rhythm()
        elif choice == "2":
            lesson_intensity()
        elif choice == "exit":
            break
        else:
            print("Invalid selection. Please choose 1, 2, or 'exit'.")


if __name__ == "__main__":
    try:
        main()
    finally:
        spi.close()
        GPIO.cleanup()
        pygame.quit()
