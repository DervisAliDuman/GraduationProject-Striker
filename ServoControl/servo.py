import RPi.GPIO as GPIO
import time

# Set the GPIO mode to use BCM numbering
GPIO.setmode(GPIO.BCM)

# Set the GPIO pins that the servos are connected to
servo1_pin = 12
servo2_pin = 13

# Set the pulse width modulation frequency
pwm_frequency = 50

# Set the minimum and maximum pulse widths
min_pulse = 0.5
max_pulse = 2.5

# Set the minimum and maximum angles for the servos
min_angle = 0
max_angle = 180

# Calculate the pulse width for the minimum and maximum angles
min_pulse_width = (min_pulse / 1000) * pwm_frequency
max_pulse_width = (max_pulse / 1000) * pwm_frequency

# Calculate the duty cycle for the minimum and maximum pulse widths
min_duty_cycle = (min_pulse_width / 20) * 100
max_duty_cycle = (max_pulse_width / 20) * 100

# Calculate the angle range
angle_range = max_angle - min_angle

# Calculate the duty cycle range
duty_cycle_range = max_duty_cycle - min_duty_cycle

# Set up the GPIO pins as outputs
GPIO.setup(servo1_pin, GPIO.OUT)
GPIO.setup(servo2_pin, GPIO.OUT)

# Create PWM instances for the servo pins
pwm1 = GPIO.PWM(servo1_pin, pwm_frequency)
pwm2 = GPIO.PWM(servo2_pin, pwm_frequency)

# Start the PWM with a duty cycle of 0
pwm1.start(0)
pwm2.start(0)

def set_servo_angle(pwm, angle):
  # Calculate the duty cycle for the desired angle
  duty_cycle = ((angle - min_angle) / angle_range) * duty_cycle_range + min_duty_cycle
  
  # Set the servo to the calculated angle
  pwm.ChangeDutyCycle(duty_cycle)

try:
  # Set the second servo to the maximum angle
  set_servo_angle(pwm2, max_angle)
  
  while True:
    # Wait for the user to press the 'x' key
    key = input("Press the 'x' key to move the first servo: ")
    if key == 'x':
      # Set the first servo to the minimum angle
      set_servo_angle(pwm1, min_angle)
      time.sleep(1)
      
      # Set the first servo to the maximum angle
      set_servo_angle(pwm1, max_angle)
      time.sleep(1)
      
except KeyboardInterrupt:
  # Clean up and exit when the user presses ctrl+c
  pwm1.stop()
  pwm2.stop()
  GPIO.cleanup()
  print("Exiting")
