import GUI
import HAL
import cv2
import numpy as np

# Enter sequential code!
kP = 0.004
kI = 0.0001
kD = 0.0001
accumulated = 0
rate = 0
prev_error = 0
while True:
    error = 0
    
    image = HAL.getImage()
    image_center_x = image.shape[1] // 2
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 100, 100])
    upper= np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower, upper)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) > 0:
        largest_contour = max(contours, key = cv2.contourArea)
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])  
            cY = int(M["m01"] / M["m00"]) 
        
        error = cX - image_center_x
        rate = error-prev_error
        accumulated = accumulated + error
        accumulated = max(min(accumulated, 1000), -1000)
        cv2.drawContours(image, [largest_contour], -1, (0, 255, 0), 2)
        cv2.circle(image, (cX, cY), 5, (0, 0, 255), -1)
        prev_error = error
    HAL.setV(10)
    HAL.setW(-error*kP + accumulated*kI + rate*kD)
    GUI.showImage(image)





