"""
Author: Rajesh Roy
Email: rajeshroy402@gmail.com
Description: This script allows you to open images from a specified folder,
             draw circles on the images using the mouse, and rename the images.
             You can navigate through the images using the 'n' and 'p' keys.
             The image can be zoomed in or out using the '+' and '-' keys.
"""

import cv2
import argparse
import os

# Function to handle mouse events
def draw_circle(event, x, y, flags, param):
    global center, drawing, edited_img, circles

    if event == cv2.EVENT_LBUTTONDOWN:
        center = (x, y)
        drawing = True

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            temp_img = edited_img.copy()
            if center is not None:  # Check if center is defined
                radius = int(((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5)
                cv2.circle(temp_img, center, radius, (0, 255, 0), 2)
            cv2.imshow(window_name, temp_img)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing:
            drawing = False
            if center is not None:  # Check if center is defined
                radius = int(((x - center[0]) ** 2 + (y - center[1]) ** 2) ** 0.5)
                circles.append((center, radius))
            redraw_image()

# Function to redraw the image with all circles
def redraw_image():
    global edited_img, display_img
    edited_img = img.copy()
    for center, radius in circles:
        cv2.circle(edited_img, center, radius, (0, 255, 0), 2)
    display_img = cv2.resize(edited_img, None, fx=zoom_scale, fy=zoom_scale)
    cv2.imshow(window_name, display_img)

# Function to rename the image
def rename_image(file_path):
    current_name = os.path.splitext(os.path.basename(file_path))[0]
    current_ext = os.path.splitext(file_path)[1]
    new_name = input(f"Enter the new name for the image (default: {current_name}): ")
    new_name = new_name if new_name else current_name
    new_path = os.path.join(os.path.dirname(file_path), new_name + current_ext)
    if os.path.isfile(new_path):
        print("A file with that name already exists.")
    else:
        cv2.imwrite(new_path, edited_img)
        print(f"Image saved as {new_path}")

# Function to load the image at the given index
def load_image(index):
    global img, edited_img, circles, window_title, display_img, zoom_scale
    img = cv2.imread(image_files[index])
    if img is None:
        print(f"Could not open or find the image: {image_files[index]}")
        exit()
    edited_img = img.copy()
    circles = []
    window_title = f"Image - {os.path.basename(image_files[index])}"
    zoom_scale = 1.0  # Reset zoom scale
    display_img = img.copy()
    cv2.imshow(window_name, display_img)

# Parse command line arguments
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Open an image, draw circles, and rename the image.')
    parser.add_argument('folder', help='Path to the folder containing images')
    args = parser.parse_args()

    # Get list of image files in the folder
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tiff')
    image_files = [os.path.join(args.folder, f) for f in os.listdir(args.folder) if f.lower().endswith(supported_formats)]
    image_files.sort()  # Sort the files for consistent order

    if not image_files:
        print(f"No images found in the folder: {args.folder}")
        exit()

    window_name = "Image Window"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # Initialize global variables
    center = None
    drawing = False
    edited_img = None
    circles = []
    display_img = None
    zoom_scale = 1.0

    current_index = 0
    load_image(current_index)

    # Set a mouse callback
    cv2.setMouseCallback(window_name, draw_circle)

    while True:
        cv2.imshow(window_name, display_img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('c') or key == ord('C'):
            print("Click to set the center, and drag to draw a circle.")
        elif key == ord('r') or key == ord('R'):
            rename_image(image_files[current_index])
        elif key == ord('u') or key == ord('U'):
            if circles:
                circles.pop()
                redraw_image()
        elif key == ord('n') or key == ord('N'):  # Move to the next image
            if current_index < len(image_files) - 1:
                current_index += 1
                load_image(current_index)
        elif key == ord('p') or key == ord('P'):  # Move to the previous image
            if current_index > 0:
                current_index -= 1
                load_image(current_index)
        elif key == ord('+'):  # Zoom in
            zoom_scale += 0.25  # Increase zoom scale by 25%
            redraw_image()
        elif key == ord('-'):  # Zoom out
            zoom_scale -= 0.25  # Decrease zoom scale by 25%
            zoom_scale = max(0.25, zoom_scale)  # Minimum zoom scale of 0.25
            redraw_image()
        elif key == 27:  # Escape key to exit
            break

    cv2.destroyAllWindows()
