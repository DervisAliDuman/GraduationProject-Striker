import cv2
import numpy as np

# Set up the webcam
cap = cv2.VideoCapture(0)

while True:
    # Get the current frame
    ret, frame = cap.read()

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the range of red color in HSV
    lower_red = np.array([0,100,100])
    upper_red = np.array([10,255,255])

    # Create a mask for the red color
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Find contours in the red mask
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    # Define the range of blue color in HSV
    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])

    # Create a mask for the blue color
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to the frame
    blur = cv2.GaussianBlur(gray, (5,5), 0)

    # Use the Hough transform to detect circles in the frame
    circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, 1, 100, param1=200, param2=20, minRadius=20, maxRadius=45)


    if len(contours_red) > 0:
        c_red = max(contours_red, key=cv2.contourArea)
        x_red,y_red,w_red,h_red = cv2.boundingRect(c_red)

        # Set the minimum and maximum length
        min_length = 20
        max_length = 200

        # Check if the rectangle is within the desired range
        if min_length < w_red < max_length and min_length < h_red < max_length:
            # Draw a rectangle around the largest contour
            cv2.rectangle(frame, (x_red, y_red), (x_red + w_red, y_red + h_red), (0, 0, 255), 2)

        # Make sure circles were detected
        if circles is not None:
            # Convert the circle coordinates to integers
            circles = np.round(circles[0, :]).astype("int")

            # Loop over the circles
            for (center_x_blue, center_y_blue, radius) in circles:
                # Draw the circle on the frame
                cv2.circle(frame, (center_x_blue, center_y_blue), radius, (0, 255, 0), 2)
                break  # <-- Add this line to break out of the loop after the first circle is detected

            # Check if the center of the blue ball is inside the red rectangle
            if x_red < center_x_blue < x_red + w_red and y_red < center_y_blue < y_red + h_red:
                print("Blue ball is inside the red rectangle")
            else:
                print("Blue ball is outside the red rectangle")


    # Display the frame
    cv2.imshow("Frame", frame)

    # Check if the user pressed "q" to quit
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

# Clean up
cap.release()
cv2.destroyAllWindows()


    
