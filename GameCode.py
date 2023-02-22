import board
import digitalio
import time
import random
from adafruit_motor import stepper

led1 = digitalio.DigitalInOut(board.A0)
led1.direction = digitalio.Direction.OUTPUT

led2 = digitalio.DigitalInOut(board.A1)
led2.direction = digitalio.Direction.OUTPUT

button1 = digitalio.DigitalInOut(board.A2)
button1.direction = digitalio.Direction.INPUT

button2 = digitalio.DigitalInOut(board.A3)
button2.direction = digitalio.Direction.INPUT

coils = (
    digitalio.DigitalInOut(board.D9),  # A1
    digitalio.DigitalInOut(board.D10),  # A2
    digitalio.DigitalInOut(board.D11),  # B1
    digitalio.DigitalInOut(board.D12),  # B2
    )

def randomizersimple():
    lednumber = [0, 1]
    x = []
    LEDs = [led1, led2]
    LEDcolor = ["red", "green"]
    buttons = [button1, button2]
    ledrandom = []
    buttonrandom = []
    ledcolor = []
    i = 0
    while i < len(lednumber):
        randomLED = random.choice(lednumber)
        if randomLED not in x:
            x.append(randomLED)
            ledrandom.append(LEDs[randomLED])
            buttonrandom.append(buttons[randomLED])
            ledcolor.append(LEDcolor[randomLED])
            i = i+1
    return ledrandom, buttonrandom, ledcolor

def randomizerLarger(flashes):
    j=0
    ledcounter = []
    for j in range(flashes):
        ledcounter.append(j)
    lednumber = [0, 1]
    x = []
    LEDs = [led1, led2]
    LEDcolor = ["red", "green"]
    buttons = [button1, button2]
    ledrandomlarge = []
    buttonrandomlarge = []
    ledcolorlarge = []
    i = 0
    while i < len(ledcounter):
        randomLED = random.choice(lednumber)
        x.append(randomLED)
        ledrandomlarge.append(LEDs[randomLED])
        buttonrandomlarge.append(buttons[randomLED])
        ledcolorlarge.append(LEDcolor[randomLED])
        i = i+1
    return ledrandomlarge, buttonrandomlarge, ledcolorlarge

def checkbutton():

    ledrandom, buttonrandom, ledcolor = randomizersimple()
    ledrandom[1].value = False
    time.sleep(2)
    for i in range(len(ledrandom)):
        ledrandom[i].value = True
        time.sleep(1)
        ledrandom[i].value = False
        time.sleep(1.0)

    STATE_WAIT_TRUE = 1
    STATE_WAIT_FALSE = 2
    STATE_CHECK = 3

    user_button_order = []
    user_color_led = []
    LEDs = [led1, led2]
    buttons = [button1, button2]
    LEDcolors = ["red", "green"]
    numberbuttons = 0
    state = STATE_WAIT_TRUE
    level = 0

    #Motor section
    DELAY = 0.01
    STEPS = 200

    for coil in coils:
        coil.direction = digitalio.Direction.OUTPUT

    motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

    while(True):
        if state is STATE_WAIT_TRUE:
            for numberbuttons in range(0, len(buttonrandom)):
                #print(numberbuttons)
                if buttons[numberbuttons].value == 1:
                    user_button_order.append(buttons[numberbuttons])
                    user_color_led.append(LEDcolors[numberbuttons])
                    print(user_color_led)
                    LEDs[numberbuttons].value = 1
                    #print("This is button state old:", buttons[numberbuttons].value)
                    state = STATE_WAIT_FALSE
                    break
        if state is STATE_WAIT_FALSE:
            #print("This is button state new:", buttons[numberbuttons].value)
            time.sleep(0.1)
            if buttons[numberbuttons].value == 0:
                LEDs[numberbuttons].value = 0
                state = STATE_WAIT_TRUE
                if len(user_button_order) == len(buttons):
                    state = STATE_CHECK
        if state is STATE_CHECK:
            if user_color_led == ledcolor:
                print("You win!")
                level = level + 1
                for step in range(STEPS):
                    motor.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
                    time.sleep(DELAY)
                motor.release()
                break
            else:
                print("You lose")
                for step in range(level * STEPS):
                    motor.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
                    time.sleep(DELAY)
                motor.release()
                break
    return level

def levels(time_between_flashes, flashes, level):

    ledrandomlarge, buttonrandomlarge, ledcolorlarge = randomizerLarger(flashes)
    ledrandomlarge[1].value = False
    time.sleep(2)
    for i in range(len(ledrandomlarge)):
        ledrandomlarge[i].value = True
        time.sleep(time_between_flashes)
        ledrandomlarge[i].value = False
        time.sleep(time_between_flashes)

    STATE_WAIT_TRUE = 1
    STATE_WAIT_FALSE = 2
    STATE_CHECK = 3

    user_button_order = []
    user_color_led = []
    LEDs = [led1, led2]
    buttons = [button1, button2]
    LEDcolors = ["red", "green"]
    numberbuttons = 0
    state = STATE_WAIT_TRUE

    #Motor section
    DELAY = 0.01
    STEPS = 200

    for coil in coils:
        coil.direction = digitalio.Direction.OUTPUT

    motor = stepper.StepperMotor(coils[0], coils[1], coils[2], coils[3], microsteps=None)

    while(True):
        if state is STATE_WAIT_TRUE:
            for numberbuttons in range(0, 2):
                #print(numberbuttons)
                if buttons[numberbuttons].value == 1:
                    user_button_order.append(buttons[numberbuttons])
                    user_color_led.append(LEDcolors[numberbuttons])
                    print(user_color_led)
                    LEDs[numberbuttons].value = 1
                    #print("This is button state old:", buttons[numberbuttons].value)
                    state = STATE_WAIT_FALSE
                    break
        if state is STATE_WAIT_FALSE:
            #print("This is button state new:", buttons[numberbuttons].value)
            time.sleep(0.1)
            if buttons[numberbuttons].value == 0:
                LEDs[numberbuttons].value = 0
                state = STATE_WAIT_TRUE
                if len(user_button_order) == len(ledcolorlarge):
                    state = STATE_CHECK
        if state is STATE_CHECK:
            if user_color_led == ledcolorlarge:
                print("You win!")
                for step in range(STEPS):
                    motor.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
                    time.sleep(DELAY)
                motor.release()
                print("Type \"Y\" to begin next round")
                print("Type \"N\" to walk away with your prize")
                choice = input("> ")
                if "Y" in choice or "y" in choice:
                    print("Next level begins now")
                    level = level + 1
                elif "N" in choice or "n" in choice:
                    print("Lame. Take your prize.")
                    for step in range(level * STEPS):
                        motor.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
                        time.sleep(DELAY)
                    motor.release()
                    level = 0
                else:
                    print("Choose!")
                break
            else:
                print(level)
                print("You lose")
                print("This is user input color vector:", user_color_led)
                print("This is actual color vector:", ledcolorlarge)
                for step in range(level * STEPS):
                    motor.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)
                    time.sleep(DELAY)
                motor.release()
                break
    return level

def opening_level():
    print("Welcome!\n")
    print("In this game you will watch a generated sequence of LEDs. ")
    print("After the sequence finishes, you will attempt to replicate the sequence ")
    print("by memory by pushing the buttons in the generated sequence.\n")
    print("The button near the red LED activates the red LED ")
    print("and the button near the green LED activates the green LED. \n")
    print("Here is a test sequence. Type \"Y\" to begin test round. Good luck!")
    choice = input("> ")
    if "Y" in choice or "y" in choice:
        level = checkbutton()
    else:
        print("Type \"Y\" to begin")
    return level

level = opening_level()

if level == 1:
    time.sleep(2)
    print("You made it! Let's start the real challenge.")
    print("Type \"Y\" to begin the next round.")
    choice = input("> ")
    if "Y" or "y" in choice:
        level = levels(0.75, 4, level)
    else:
        print("Type \"Y\" to begin.")


if level == 2:
    print("Hey, you're pretty good at this! Try this:")
    print("Type \"Y\" to begin the next round.")
    choice = input("> ")
    if "Y" or "y" in choice:
        level = levels(0.5, 5, level)
    else:
        print("Type \"Y\" to begin")

if level == 3:
    print("Wow, you made it to the final level!")
    print("Try this:")
    print("Type \"Y\" to begin the next round.")
    choice = input("> ")
    if "Y" or "y" in choice:
        level = levels(0.4, 8, level)
    else:
        print("Type \"Y\" to begin")

if level == 4:
    print("Congrats!!! You win the grand prize!")
    print("Enjoy your pop tart :\)!")


