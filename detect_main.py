## ctrl +c to stop process
import os
import GUI
import Xmem
import overlay
from multiprocessing import Process

def run_segment(first_frame_path,directory, boundary):
    Xmem.segment(first_frame_path,directory, boundary)

def main(folder_name):

    ## Select the frames by GUI
    print("Please select the first frame")

    overlay.overlay_save(os.path.join('workspace', folder_name, 'images', 'img.jpg' ), os.path.join('workspace', folder_name, 'masks', 'img.png'))

    first_frame_path = os.path.join('workspace', folder_name, 'masks', 'img.png')
    first_frame_path_colored = os.path.join('workspace', folder_name, 'overlay.png')

    ## Select the boundary by the first frame 
    boundary = GUI.select_points(first_frame_path_colored)

    ## go the the directory where masks are stored
    directory_to_watch = os.path.join("./saving_frame",folder_name)
    if not os.path.exists(directory_to_watch):
        os.makedirs(directory_to_watch)

    ## Using Multithread to run Xmem model in the background
    p = Process(target=run_segment, args=(first_frame_path, directory_to_watch, boundary))
    p.start()

    p.join()

if __name__ == "__main__":
    main()