#!/usr/bin/env python3
from ev3dev2.motor import MoveTank, OUTPUT_B, OUTPUT_C, SpeedPercent, LargeMotor, Motor, MoveSteering
from ev3dev2.sensor.lego import ColorSensor, UltrasonicSensor, TouchSensor
from ev3dev2.sound import Sound
from time import sleep

tank_pair = MoveTank(OUTPUT_B, OUTPUT_C)
cl = ColorSensor()
sound = Sound()
count = 0
ts = TouchSensor()
us = UltrasonicSensor()
us.mode = 'US-DIST-CM'
steer_pair = MoveSteering(OUTPUT_B, OUTPUT_C)
mLeft = LargeMotor(OUTPUT_B)
mRight = LargeMotor(OUTPUT_C)

#Return when we find black so the check function is called again
def adjust():
    #Firstly move forward a small amount, as this seems to be a reccuring issue
    tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 0.2)

    if cl.color == 1 or cl.reflected_light_intensity < 25:
        return

    #Reverse to where we were before error occured (Intentionally does not account for the initial nudge forward)
    tank_pair.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), 1.15)

    #Adjust, first to the left
    tank_pair.on_for_rotations(SpeedPercent(0), SpeedPercent(40), 0.1)

    #Move forward and check again
    tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 1.15)

    if cl.color == 1 or cl.reflected_light_intensity < 25:
        return

    #Move back to where we were
    tank_pair.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), 1.15)

    #Adjust, to the right, to the same degree
    tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(0), 0.2)

    #Move forward again
    tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 1.15)

    if cl.color == 1 or cl.reflected_light_intensity < 25:
        return

    #Move back where we were
    tank_pair.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), 1.15)

    #Larger adjust to the left also accounting for previous step
    tank_pair.on_for_rotations(SpeedPercent(0), SpeedPercent(40), 0.3)

    # Move forward again
    tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 1.15)

    if cl.color == 1 or cl.reflected_light_intensity < 25:
        #Adjust right slightly to account for larger angle
        tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(0), 0.1)
        return

    # Move back to where we were
    tank_pair.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), 1.15)

    # Larger adjust to the right also accounting for previous step
    tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(0), 0.4)

    # Move forward again
    tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 1.15)

    if cl.color == 1 or cl.reflected_light_intensity < 25:
        #Adjust left slightly to account for larger angle
        tank_pair.on_for_rotations(SpeedPercent(0), SpeedPercent(40), 0.1)
        return
    else:
        #reverse and correct angle
        tank_pair.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), 1)
        tank_pair.on_for_rotations(SpeedPercent(0), SpeedPercent(40), 0.2)
        #Try again (We will be slightly further forward than last time)
        adjust()

def check():
    # If colour is black
    if cl.color == 1 or cl.reflected_light_intensity < 25:
        return True
    else:
        #Error checking
        adjust()
        #Check again
        check()

#Get from S tile to the starting black tile

#Move forward
tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 0.6)
#Turn right
tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(0), 1)
#Reverse
tank_pair.on_for_rotations(SpeedPercent(-40), SpeedPercent(-40), 0.5)

while count < 15:
    #If we find black
    if check():
        #increase count and beep to indicate doing so
        count += 1
        sound.beep()

        if count < 15:
            #Move forward
            tank_pair.on_for_rotations(SpeedPercent(40), SpeedPercent(40), 1.15)

#Turn 90 degrees to the right
tank_pair.on_for_rotations(SpeedPercent(50), SpeedPercent(0), 1)

#PART TWO

def ultracheck(steer):

    #Turn left 50 degrees
    mRight.on_for_degrees(SpeedPercent(30), degrees=125)
    sleep(0.5)
    #Take ultrasonic measurement
    dist_left = us.distance_centimeters_continuous
    #Turn back to the middle
    mRight.on_for_degrees(SpeedPercent(-30), degrees=125)
    sleep(0.5)
    #Take ultrasonic measurement
    odist = us.distance_centimeters_continuous
    #Turn right
    mLeft.on_for_degrees(SpeedPercent(30), degrees=125)
    sleep(0.5)
    #Take measurement
    dist_right = us.distance_centimeters_continuous
    #Turn back to the middle
    mLeft.on_for_degrees(SpeedPercent(-30), degrees=125)
    sleep(0.5)

    # If the closest reading was to the left
    if dist_left < dist_right and dist_left < odist:
        steer_pair.on_for_seconds(steering=-steer, speed=15, seconds=1)
    # If the closest reading was to the right
    elif dist_right < dist_left and dist_right < odist:
        steer_pair.on_for_seconds(steering=steer, speed=15, seconds=1)
    #Closest in the middle
    elif odist < dist_left and odist < dist_right:
        sound.beep()
    else:
        #Can't determine
        tank_pair.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 0.5)
        # Check distances with a tiny correction
        ultracheck(steer)

#Move forward 10 rotations to get close to tower
tank_pair.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 7)

#Check distances with a large correction
ultracheck(30)

#Move forward after adjusting
tank_pair.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 2)

#Check distances with a medium correction
ultracheck(20)

#Move forward after adjusting
tank_pair.on_for_rotations(SpeedPercent(30), SpeedPercent(30), 2)

#Check distances with a small correction
ultracheck(15)

#Ram tower at high speed
tank_pair.on_for_rotations(SpeedPercent(80), SpeedPercent(80), 6)

#Report completion
sound.speak("Completed")



























































