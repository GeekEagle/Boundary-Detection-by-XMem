from PIL import Image, ImageEnhance
import numpy as np
import cv2
import os

def cv2_to_pil(cv2_image):
    rgb_image = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
    pil_image = Image.fromarray(rgb_image)
    return pil_image

def pil_to_cv2(pil_image):
    image_array = np.array(pil_image)
    cv2_image = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
    return cv2_image

def overlay_save(image_path, mask_path):

    # Load the image and mask
    image = Image.open(image_path)
    mask = Image.open(mask_path).convert("RGBA")

    # Overlay the mask on the image
    mask.putalpha(90)
    image.paste(mask, (0, 0), mask)

    # Increase brightness by 70%
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.7)
    
    image.save(os.path.join(os.path.dirname(os.path.dirname(mask_path)), 'overlay.png'))


def overlay(frame, mask):
    ## default => opened by PIL

    # Overlay the mask on the image
    mask.putalpha(90)
    frame.paste(mask, (0, 0), mask)

    # Increase brightness by 70%
    enhancer = ImageEnhance.Brightness(frame)
    frame = enhancer.enhance(1.7) 
    frame = pil_to_cv2(frame)
    
    # return a cv2 result
    return frame

if __name__ == '__main__':
    overlay_mask('card_org.jpg', 'card.png')