import cv2
import numpy as np
import sys

# Check if image name is provided as command line argument
if len(sys.argv) != 2:
    print("Usage: python dot_tagger.py <image_name>")
    sys.exit(1)

# Load the image
image_name = sys.argv[1]
image = cv2.imread(image_name)

# Create a window for the image
cv2.namedWindow('Image', cv2.WINDOW_NORMAL)

# Initialize dot counts
red_count = 0
green_count = 0
yellow_count = 0

# Initialize current color
current_color = (0, 0, 255)  # Red

# Store dot positions and colors
dots = []

def draw_dot(event, x, y, flags, param):
    global red_count, green_count, yellow_count
    if event == cv2.EVENT_LBUTTONDOWN:
        dots.append((x, y, current_color))
        cv2.circle(image, (x, y), 2, current_color, -1)  # Decreased dot size
        if current_color == (0, 0, 255):
            red_count += 1
        elif current_color == (0, 255, 0):
            green_count += 1
        elif current_color == (0, 255, 255):
            yellow_count += 1
        print(f'Red: {red_count}, Green: {green_count}, Yellow: {yellow_count}')

def undo_dot():
    global red_count, green_count, yellow_count
    if dots:
        x, y, color = dots.pop()
        cv2.circle(image, (x, y), 2, (255, 255, 255), -1)  # Draw white circle to remove dot
        if color == (0, 0, 255):
            red_count -= 1
        elif color == (0, 255, 0):
            green_count -= 1
        elif color == (0, 255, 255):
            yellow_count -= 1
        print(f'Red: {red_count}, Green: {green_count}, Yellow: {yellow_count}')

cv2.setMouseCallback('Image', draw_dot)

while True:
    # Display the image
    cv2.imshow('Image', image)

    # Wait for key press
    key = cv2.waitKey(1)

    # Exit on 'q' press
    if key == ord('q'):
        break

    # Change color on '1', '2', '3' press
    elif key == ord('1'):
        current_color = (0, 0, 255)  # Red
    elif key == ord('2'):
        current_color = (0, 255, 0)  # Green
    elif key == ord('3'):
        current_color = (0, 255, 255)  # Yellow

    # Undo on 'z' press
    elif key == ord('z'):
        undo_dot()

# Close all OpenCV windows
cv2.destroyAllWindows()
