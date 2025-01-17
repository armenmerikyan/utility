import pyautogui
from PIL import Image
import numpy as np
import pyautogui
import time
import keyboard

def capture_region(region):
    """
    Captures a screenshot of the specified region.
    Args:
        region (tuple): A tuple (x, y, width, height) defining the region to capture.
    Returns:
        Image: The captured region as a Pillow Image object.
    """
    screenshot = pyautogui.screenshot(region=region)
    return screenshot

def check_for_color(image, color_thresholds):
    """
    Checks if the image contains specific colors.
    Args:
        image (Image): The Pillow Image object to analyze.
        color_thresholds (dict): Thresholds for colors as (min, max) for each channel.
                                 Example: {'red': [(150, 255), (0, 100), (0, 100)],
                                           'green': [(0, 100), (150, 255), (0, 100)]}
    Returns:
        list: A list of detected colors in the image.
    """
    # Convert the image to a numpy array
    img_array = np.array(image)
    
    detected_colors = []
    for color_name, thresholds in color_thresholds.items():
        # Create masks for the given color
        mask = (
            (img_array[:, :, 0] >= thresholds[0][0]) & (img_array[:, :, 0] <= thresholds[0][1]) &
            (img_array[:, :, 1] >= thresholds[1][0]) & (img_array[:, :, 1] <= thresholds[1][1]) &
            (img_array[:, :, 2] >= thresholds[2][0]) & (img_array[:, :, 2] <= thresholds[2][1])
        )
        if mask.any():
            detected_colors.append(color_name)
    
    return detected_colors

# Define the region to capture (x, y, width, height)
region_to_capture = (1402, 446, 100, 50)  # Example values, adjust as needed

# Define color thresholds
color_thresholds = {
    'red': [(150, 255), (0, 100), (0, 100)],  # Red
    'green': [(0, 100), (150, 255), (0, 100)]  # Green
}

def backspace_loop(times):
    for _ in range(times):
        keyboard.send('backspace')
        time.sleep(0.1)

while True :

    time.sleep(60)
    # Capture the region
    captured_image = capture_region(region_to_capture)

    # Check for colors
    detected_colors = check_for_color(captured_image, color_thresholds)

    # Output the result
    if detected_colors:
        print(f"Detected colors: {', '.join(detected_colors)}")

        if 'red' not in detected_colors:
            pyautogui.click(226, 41)
            time.sleep(0.2)
            pyautogui.click(95, 82)
            time.sleep(2)

            pyautogui.click(1804, 456) # sell 
            time.sleep(0.5)
            pyautogui.click(759, 698) # advanced button 
            time.sleep(0.5)
            pyautogui.click(1123, 315) # s1 sale button
            time.sleep(0.5)
            pyautogui.click(1122, 446) #99 %
            time.sleep(0.5)


            pyautogui.click(821, 755) #99 %
            time.sleep(0.5)
            backspace_loop(8)
            time.sleep(0.5)            
            pyautogui.typewrite("0.0001")
            
            pyautogui.click(806, 823) #99 %
            time.sleep(0.5)            
            backspace_loop(8)
            time.sleep(0.5)            
            pyautogui.typewrite("0.0001")
            time.sleep(5)
            pyautogui.click(830, 901) # sell
            time.sleep(2)
            pyautogui.click(1231, 125) # x pop up
            time.sleep(0.2)
            #pyautogui.click(1866, 460) # hide
            #time.sleep(0.5)

            pyautogui.click(95, 82)
            time.sleep(5)
        
    #else:
    #    print("i")
    
    
    time.sleep(0.1)
