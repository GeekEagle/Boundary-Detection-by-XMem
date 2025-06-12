import cv2
from inference.interact.interactive_utils import *
import torch
import numpy as np
import os
from PIL import Image

from model.network import XMem
from inference.inference_core import InferenceCore

import matplotlib.pyplot as plt

import overlay
import find

torch.set_grad_enabled(False)

# default configuration
config = {
    'top_k': 30,
    'mem_every': 5,
    'deep_update_every': -1,
    'enable_long_term': True,
    'enable_long_term_count_usage': True,
    'num_prototypes': 128,
    'min_mid_term_frames': 5,
    'max_mid_term_frames': 10,
    'max_long_term_elements': 10000,
}

def natural_sort_key(s):
    import re
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def segment(first_frame_path, directory, boundary):

    network = XMem(config, 'saves\XMem.pth').eval().to(device)
    torch.cuda.empty_cache()

    mask_name = first_frame_path

    mask = np.array(Image.open(mask_name))
    print(np.unique(mask))
    num_objects = len(np.unique(mask)) - 1

    processor = InferenceCore(network, config=config)
    processor.set_all_labels(range(1, num_objects + 1))  # consecutive labels

    ## change here to switch camera
    cap = cv2.VideoCapture(0)
    
    total_frames = 1000000

    # You can change these two numbers
    frames_to_propagate = total_frames
    ## change this would skip frames
    visualize_every = 1

    current_frame_index = 0

    with torch.cuda.amp.autocast(enabled=True):
        while (cap.isOpened()):
            # load frame-by-frame
            _, frame = cap.read()
            frame = cv2.flip(frame, 1)
        
            if frame is None or current_frame_index > frames_to_propagate:
                break
            
            # convert numpy array to pytorch tensor format
            frame_torch, _ = image_to_torch(frame, device=device)
            if current_frame_index == 0:
                # initialize with the mask
                mask_torch = index_numpy_to_one_hot_torch(mask, num_objects + 1).to(device)
                # the background mask is not fed into the model
                prediction = processor.step(frame_torch, mask_torch[1:])
            
            else:
                # propagate only
                ## skip frames not needed 
                if (current_frame_index % visualize_every) != 0:
                    current_frame_index += 1
                    #print("skip frame {}".format(current_frame_index))
                    continue
                prediction = processor.step(frame_torch)

            # argmax, convert to numpy
            prediction = torch_prob_to_numpy_mask(prediction)

            if current_frame_index % visualize_every == 0:
                black_background_frame = np.zeros_like(frame)
                visualization = overlay_davis(black_background_frame, prediction)

                ## this is the cv2 format of the mask
                m = overlay.pil_to_cv2(Image.fromarray(visualization))
                ## this is the cv2 format of the frame 
                f = overlay.cv2_to_pil(frame)

                find.detect_live(m, f, boundary, 20)

                Image.fromarray(visualization).save('{}/{:06d}.jpg'.format(directory,current_frame_index))

            current_frame_index += 1
    