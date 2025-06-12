import cv2
import numpy as np
import time
import overlay
from inference.interact.interactive_utils import *
    
def detect_live(image, frame, boundary, fps):

    # image => mask
    # frame => orignal  

    # Convert to grayscale image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to separate non-black areas
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # set boundaries
    top = int(boundary[0])
    bottom = int(boundary[1])
    left = int(boundary[2])
    right = int(boundary[3])

    boundary = {'left': left, 'top': top, 'right': right, 'bottom': bottom}

    # Check the boundaries
    out_of_bounds_objects = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        # Check if the object is out of the boundary
        if (x < boundary['left'] or 
            x + w > boundary['right'] or
            y < boundary['top'] or 
            y + h > boundary['bottom']):
            out_of_bounds_objects.append(contour)
                
    if not contours:
            # Assume frame is a PIL Image, get its dimensions
            width, height = frame.size
            # Consider the entire image as out of bounds
            out_of_bounds_objects.append(np.array([[0, 0], [width, 0], [width, height], [0, height]]))
    
    out_of_bounds = out_of_bounds_objects
    
# Call the function and pass the image path

# Print the results
    if out_of_bounds:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        # print("Some objects are out of the boundary.")
    else:
        cv2.rectangle(image, (left, top), (right, bottom), (0, 255, 0), 2)
    
    image = overlay.cv2_to_pil(image)
    image = overlay.overlay(frame, image)

    cv2.imshow('Image with Boundary', image)

    ## set fps here
    cv2.waitKey(1)  # Wait for a key press to proceed