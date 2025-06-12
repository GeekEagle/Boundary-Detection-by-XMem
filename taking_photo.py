import cv2
import os
import datetime

def main():

    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Failed to open camera")
        return
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    print("Pressing enter to take photo, pressing esc to exit.")
    
    while True:
        now = datetime.datetime.now()
        __, frame = cap.read()

        frame = cv2.flip(frame, 1)

        cv2.imshow("Press Enter to Capture", frame)
        key = cv2.waitKey(1)

        if key == 13:
            frame_name = str(now.hour)+"_"+str(now.minute)+"_"+str(now.second)+".jpg"
            folder_name = frame_name.split(".")[0]
            photo_path = os.path.join('./workspace',folder_name)

            if not os.path.exists(photo_path):
                os.makedirs(photo_path)
                image_dir = os.path.join(photo_path, 'images')
                mask_dir = os.path.join(photo_path, 'masks')
                os.makedirs(image_dir)
                os.makedirs(mask_dir)

            cv2.imwrite("./{}/{}".format(image_dir,'img.jpg'), frame)
            break

        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

    return folder_name