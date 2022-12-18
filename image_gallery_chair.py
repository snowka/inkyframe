# An offline image gallery that switches between five jpg images
# Copy them into your Pico's flash using Thonny.
# If you want to use your own images they must be 600 x 448 pixels or smaller
# and saved as *non-progressive* jpgs

from pimoroni import ShiftRegister
from picographics import PicoGraphics, DISPLAY_INKY_FRAME
from machine import Pin
import jpegdec

# you can change your file names here
IMAGE_A = "The Chair is In.jpg"
IMAGE_B = "The Chair is Out.jpg"
IMAGE_C = "The Chair is Working Magic.jpg" 
IMAGE_D = "The Chair is In.jpg"
IMAGE_E = "The Chair is Out.jpg"
 
# set up the display
display = PicoGraphics(display=DISPLAY_INKY_FRAME)

# Inky Frame uses a shift register to read the buttons
SR_CLOCK = 8
SR_LATCH = 9
SR_OUT = 10

sr = ShiftRegister(SR_CLOCK, SR_LATCH, SR_OUT)

# set up the button LEDs
button_a_led = Pin(11, Pin.OUT)
button_b_led = Pin(12, Pin.OUT)
button_c_led = Pin(13, Pin.OUT)
button_d_led = Pin(14, Pin.OUT)
button_e_led = Pin(15, Pin.OUT)

# and the activity LED
activity_led = Pin(6, Pin.OUT)

# set up and enable vsys hold so we don't go to sleep
HOLD_VSYS_EN_PIN = 2

hold_vsys_en_pin = Pin(HOLD_VSYS_EN_PIN, Pin.OUT)
hold_vsys_en_pin.value(True)

# Create a new JPEG decoder for our PicoGraphics
j = jpegdec.JPEG(display)

# setup
activity_led.on()
# update the image on Inky every time it's powered up
# comment these lines out if running on battery power
# button_a_led.on()
# display_image(IMAGE_A)


def display_image(filename):

    # Open the JPEG file
    j.open_file(filename)

    # Decode the JPEG
    j.decode(0, 0, jpegdec.JPEG_SCALE_FULL)

    # Display the result
    display.update()


while True:
    button_a_led.off()
    button_b_led.off()
    button_c_led.off()
    button_d_led.off()
    button_e_led.off()

    # read the shift register
    # we can tell which button has been pressed by checking if a specific bit is 0 or 1
    result = sr.read()
    button_a = sr[7]
    button_b = sr[6]
    button_c = sr[5]
    button_d = sr[4]
    button_e = sr[3]

    # light up the activity LED when Inky is awake
    activity_led.on()

    if button_a == 1:
        button_a_led.on()
        display_image(IMAGE_A)
    elif button_b == 1:
        button_b_led.on()
        display_image(IMAGE_B)
    elif button_c == 1:
        button_c_led.on()
        display_image(IMAGE_C)
    elif button_d == 1:
        button_d_led.on()
        display_image(IMAGE_D)
    elif button_e == 1:
        button_e_led.on()
        display_image(IMAGE_E)

    # Go to sleep if on battery power
    activity_led.off()
    hold_vsys_en_pin.init(Pin.IN)
