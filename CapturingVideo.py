import cv2

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Check if the camera opened successfully
if not cap.isOpened(): 
    print("Unable to read camera feed")

# Default resolutions of the frame are obtained.
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

while(True):
    ret, frame = cap.read()

    if ret: 
        # Display the resulting frame    
        cv2.imshow('frame', frame)

        # Press Q on the keyboard to stop recording
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break  

# When everything is done, release the video capture and video write objects
cap.release()

# Closes all the frames
cv2.destroyAllWindows() 
