import cv2

# Start capturing video from the default camera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)


while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    print(frame.shape)

    # If frame is read correctly `ret` is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    # Display the resulting frame
    cv2.imshow('Image', frame)

    # Wait for a key press for 1ms, and if it's the 'q' key, exit the loop
    if cv2.waitKey(1) == ord('q'):
        break

# When everything is done, release the capture and close any open windows
cap.release()
cv2.destroyAllWindows()
