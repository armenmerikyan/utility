import time
import pyautogui
import pyperclip
import hashlib
import requests
from urllib.parse import quote
import json

import openai
import subprocess
import os

from PIL import Image
import numpy as np
from pynput import keyboard


model_engine = "gpt-3.5-turbo-16k"

api_key = os.getenv('open_ai_api_key')


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

def get_count_by_name_and_value(name, value):

    base_url = "https://gamebackrooms.com/get_count/"

    encoded_name = quote(name)
    encoded_value = quote(value)

    # Construct the URL for the GET request
    url = f"{base_url}?column_name={encoded_name}&value={encoded_value}"

    try:
        # Make the GET request
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        occurrences = data.get('occurrences', 0)
        return occurrences    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



def rate_meme(name, symbol):
    openai.api_key = api_key

    # Construct the content for GPT-3
    content = (
        f"rate this meme token based on its name and symbol from 1 to 100. "
        f"Name: '{name}' Symbol: '{symbol}', in 140 characters or less, tell me why you have given that rating. "
        f"Check for spelling errors, grammar mistakes, and if the meme is funny. "
        f"Respond with a JSON message indicating 'rating' and 'reasoning', like: "
        f"{{\"rating\": 95, \"reasoning\": \"sample explanation\"}}"
    )

    content_role = "You are an expert on meme tokens."

    # Call GPT-3 model
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=[
            {"role": "system", "content": content_role},
            {"role": "user", "content": content},
        ]
    )

    # Parse GPT-3 response
    message_gpt = response.choices[0]['message']['content']
    
    try:
        parsed_data = json.loads(message_gpt)
        rating = parsed_data.get("rating")
        reasoning = parsed_data.get("reasoning")
    except json.JSONDecodeError:
        raise ValueError("The response from GPT could not be parsed as JSON.")
    
    # Return rating and reasoning
    return rating, reasoning


def tweet_ticker(mint, name, symbol, rating):


    pyautogui.click(474, 64)
    time.sleep(1)
    pyautogui.click(338, 930)
    time.sleep(1)

    pyperclip.copy(rating + " Just bought bought 0.0333 sol of " + name + " $" + symbol + " CA: " +  mint + " " + "https://pump.fun/coin/" + mint)
    time.sleep(1)

    subprocess.call(['osascript', '-e', 'tell application "System Events" to keystroke "v" using command down'])
    time.sleep(1)

    pyautogui.hotkey('command', 'enter')
    time.sleep(1)

    pyautogui.click(264, 65)


    
def fetch_token_info(mint_address):
    print("fetch_token_info")
    url = f"https://gamebackrooms.com/token/{mint_address}/"
    headers = {"Accept": "application/json"}
    try:
        response = requests.get(url, headers=headers, timeout=2)  # Timeout set to 10 seconds
        response.raise_for_status()  # Raise an exception for HTTP errors
        print(response.text)
        data = response.json()
        print(json.dumps(data, indent=4))
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching token info: {e}")

def hash_mint(mint):
    """Generate a hash for the mint value."""
    return hashlib.sha256(mint.encode()).hexdigest()

def on_press(key):
    global running
    try:
        if key.char == "q":  # Press 'q' to exit
            running = False
    except AttributeError:
        pass
 

pyautogui.click(143, 413)

running = True

listener = keyboard.Listener(on_press=on_press)
listener.start()

def main():
    # Set to store hashes of all seen mints
    print("main")
    seen_mints = set()
    while running:                        
        try:
 
            # Simulate the clicks and get the current mint value
            for loop_count in range(0, 6):  # Loop from 1 to 3 (inclusive)
                print(f"Loop count: {loop_count}")

                pyautogui.click(143, 415 + (loop_count * 112))  # Click to copy mint
                time.sleep(0.1)           # Wait for clipboard to update
                mint = pyperclip.paste()  # Get the copied mint value
                time.sleep(0.05) 
                print(mint)
                # Generate hash for the mint value
                if mint is not None:
                    mint_hash = hash_mint(mint)

                    # Process only if the mint hash is new
                    if mint_hash not in seen_mints:
                        print(f"New mint detected: {mint}") 
                        
                        data = fetch_token_info(mint) 
                        print(f"New mint detected 3: {mint}")
                        pyautogui.click(506, 393 + (loop_count * 112)) 
                        print("make purchase")
                        print("-----------------------------------------------------------------------------------------------")
                        seen_mints.add(mint_hash)
                        
                pyautogui.click(276, 329)
                time.sleep(0.05)  # Delay before the next iteration

            time.sleep(1.3)

            '''    
            # Define the region to capture (x, y, width, height)
            region_to_capture = (1231, 464, 100, 50)  # Example values, adjust as needed

            # Define color thresholds
            color_thresholds = {
                'red': [(150, 255), (0, 100), (0, 100)],  # Red
                'green': [(0, 100), (150, 255), (0, 100)]  # Green
            }

            while True :
                pyautogui.click(728, 65)
                time.sleep(0.5)

                # Capture the region
                captured_image = capture_region(region_to_capture)
                #captured_image.show()

                #time.sleep(40)
                # Check for colors
                detected_colors = check_for_color(captured_image, color_thresholds)

                # Output the result
                if detected_colors:
                    print(f"Detected colors: {', '.join(detected_colors)}")

                    if 'red' in detected_colors:
                        pyautogui.click(1582, 483)
                        time.sleep(0.5)
                        pyautogui.click(1028, 642)
                        time.sleep(0.5)
                        pyautogui.click(735, 789)
                        time.sleep(0.5)
                        pyautogui.click(1123, 321)
                        time.sleep(0.5)

                else:
                    print("No target colors detected.")
                    break    
                
            
            pyautogui.click(288, 65)
            '''
        except KeyboardInterrupt:
            print("Screen monitoring stopped.")
            break  # Exit the loop
        except Exception as e:
            print(f"An error occurred: {e}")  # Keep going for other exceptions
            # Optionally handle the exception further if needed



if __name__ == "__main__":
    main()


listener.stop()