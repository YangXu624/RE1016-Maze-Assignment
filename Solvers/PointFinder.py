"""
This Python program can display the specified maze image.
"""

import cv2  # install opencv-python package to use cv2
import matplotlib.pyplot as plt  # install matplotlib package to use pyplot

"""
your maze - dijkstra_maze.png --- TO CHANGE FOR YOUR MAZE DESIGN ---
"""
# img = cv2.imread('mazes/dijkstra_maze.png')  # read an image from a file using
# cv2.circle(img, (40, 35), 3, (0, 0, 255), -1)  # add a circle at (40, 35) - blue - YOUR START POINT
# cv2.circle(img, (180, 190), 3, (255, 0, 0), -1)  # add a circle at (180, 190) - red - YOUR END POINT

img = cv2.imread('mazes/dijkstra_maze.png')  # read an image from a file using
# cv2.circle(img, (40, 35), 3, (0, 0, 255), -1)  # add a circle at (40, 35) - start point - blue
# cv2.circle(img, (180, 190), 3, (255, 0, 0), -1)  # add a circle at (180, 190) - end point - red

plt.figure()
plt.imshow(img)  # show the image
plt.show()
