import numpy as np
import math

coordinates = np.array([2, 3, 0])

thetaX = math.radians(float(input("Rotation about X axis: ")))
thetaY = math.radians(float(input("Rotation about Y axis: ")))
thetaZ = math.radians(float(input("Rotation about Z axis: ")))

rotationX = np.array([[1, 0, 0], [0, math.cos(thetaX), -math.sin(thetaX)], [0, math.sin(thetaX), math.cos(thetaX)]])
rotationY = np.array([[math.cos(thetaY), 0, math.sin(thetaY)], [0, 1, 0], [-math.sin(thetaY), 0, math.cos(thetaY)]])
rotationZ = np.array([[math.cos(thetaZ), -math.sin(thetaZ), 0], [math.sin(thetaZ), math.cos(thetaZ), 0], [0, 0, 1]])

rotation = ((rotationX @ rotationY) @ rotationZ)

result = rotation@coordinates
print(f"Coordinates after rotation w.r.t. original frame are {round(result[0], 4), round(result[1], 4), round(result[2], 4)}")
