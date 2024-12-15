import cv2
import time
from os import mkdir, path
import win32gui
import win32con

# Ensure the "footages" directory exists
if not path.exists('footages'):
    mkdir('footages')

# Minimize the current window
def minimize_window():
    window = win32gui.GetForegroundWindow()
    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

# Function to start the CCTV application
def cctv():
    # Open the video capture (default camera)
    video = cv2.VideoCapture(0)
    
    # Check if the camera is available
    if not video.isOpened():
        print("Error: Unable to access the camera. Please check your device.")
        return

    # Set camera resolution
    video.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"Video resolution is set to: {width} x {height}")
    print("--Help:  1. Press 'Esc' to exit CCTV\n2. Press 'M' to minimize the window.")

    # Video writer setup
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # Format the filename safely (replace ':' with '-')
    date_time = time.strftime("recording_%H-%M-%S_%d-%m-%Y")
    output = cv2.VideoWriter(f'footages/{date_time}.mp4', fourcc, 20.0, (width, height))

    while video.isOpened():
        ret, frame = video.read()
        if ret:
            # Flip the frame for a mirror view
            frame = cv2.flip(frame, 1)
            
            # Add timestamp overlay
            timestamp = time.strftime("%H:%M:%S, %d-%m-%Y")
            cv2.putText(frame, "Camera 1", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.putText(frame, timestamp, (10, height - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

            # Show the video feed
            cv2.imshow('CCTV Camera', frame)
            output.write(frame)

            # Handle key presses
            key = cv2.waitKey(1)
            if key == 27:  # 'Esc' key
                print("Video footage saved in 'footages' folder. Stay safe!")
                break
            elif key == ord('m'):  # 'M' key
                minimize_window()
        else:
            print("Error: Unable to capture video. Exiting...")
            break

    # Release resources
    video.release()
    output.release()
    cv2.destroyAllWindows()

# Entry point of the program
print("*" * 80)
print(" " * 30 + "Welcome to CCTV Software")
print("*" * 80)

try:
    choice = int(input("Do you want to start the CCTV?\n1. Yes\n2. No\n>>> "))
    if choice == 1:
        cctv()
    elif choice == 2:
        print("Goodbye! Stay safe!")
    else:
        print("Invalid choice. Exiting...")
except ValueError:
    print("Invalid input. Please enter a number.")
