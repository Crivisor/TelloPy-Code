from djitellopy import tello
import time

drone = tello.Tello()
drone.connect()

boxSize = 50 # Change: In Cm

# Don`t change [
# Directions
left = "left"
right = "right"
forward = "forward"
backward = "backward"
# Rotation
rotate = "rotate"
# Flip
flip = "flip"
# Land
land = "land"
# ]

# Routs (Change)
myRout = [
    # The syntax is [direction, amount of squares]
    # For rotation you have to write: [rotate, angle]
    # Negative angles for counter clockwise/Positive angles for clockwise rotations
    # For flipping write: [flip, dir(left, right, forward, backward)]
    # And if you want to land for a certain amount of time add the syntax [land, amount in secs]
    # Note: When the rout is done no need to write anything it will land automatically
    # Example:
    [right, 2], [forward, 3], [land, 5],
    [forward, 3], [left, 3], [land, 5],
    [forward, 3], [right, 3], [land, 5],
    [backward, 9], [left, 2],
    [rotate, left, 50] # Example for rotation syntax
    [flip, backward] # Example to flip backward
]

# Move function
def move (dir, amount):
    distance = amount * boxSize
    if distance < 600:
        if dir == forward:
            drone.move_forward(distance)
        
        elif dir == left:
                drone.move_left(distance)
                
        elif dir == right:
                drone.move_right(distance)
                
        elif dir == backward:
            drone.move_back(distance)
    else:
        count = 0

        while True:
            count += 1

            if distance / count < 600:
                break
        
        for i in range(0, count):
            if dir == forward:
                drone.move_forward(int(distance / count))
                
            elif dir == left:
                drone.move_left(int(distance / count))
                
            elif dir == right:
                drone.move_right(int(distance / count))
                
            elif dir == backward:
                drone.move_back(int(distance / count))

# Rotate
def rotate_ (angle: int):
    if angle > 0:
        drone.rotate_clockwise(angle)
    else:
        drone.rotate_counter_clockwise(angle)

# Flip
def flipDrone (dir):
    if dir == forward:
        drone.flip_forward()
        
    elif dir == backward:
        drone.flip_back()
         
    elif dir == left:
        drone.flip_left()

    else:
        drone.flip_right()

# Land
def landFor (secs):
    drone.land()
    time.sleep(secs)
    drone.takeoff()

# Read rout then move function
def readRoutAndMove (rout: list):
    for i in range(0, len(rout)):
        if rout[i][0] == land:
            landFor(rout[i][1])

        if rout[i][0] == rotate:
            rotate_(rout[i][1], rout[i][2])

        if rout[i][0] == flip:
            flipDrone(rout[i][1])

        else:
            move(rout[i][0], rout[i][1])

while True:
    inp = input("What do you want?(B for battery percentage/Anything else to start code)\n>").strip().capitalize()

    if inp[0] == "B": 
        # To know the battery
        print(drone.get_battery())
    else:
        # Important
        drone.takeoff()
        # Rout thingy
        readRoutAndMove(myRout) # Replace with correct rout
        # Important
        drone.land()