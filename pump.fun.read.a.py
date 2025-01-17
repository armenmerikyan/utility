import asyncio
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
import time
from urllib.parse import urlparse
import aiohttp
import requests
from bs4 import BeautifulSoup
import os
import uuid
import threading
import sys
import json

LOGIN_USERNAME_0192 = ' '
LOGIN_PASSWORD_0192 = ' '
username = ' '
password = ' '

login_data = {
    'username': LOGIN_USERNAME_0192,
    'password': LOGIN_PASSWORD_0192
} 


url_main = "http://gamebackrooms.com"
url_topics = url_main + "/topics/"  # Update with your actual URL
url_login = url_main + "/login/"
url_convo = url_main + "/api/convo-log/"
url_conversation_topics = url_main + '/api/conversation-topics/'

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Path to your GeckoDriver executable
webdriver_path = "/Users/armenmerikyan/Desktop/wd/gh/geckodriver"  # Update with the path to your GeckoDriver

# URL of the webpage to monitor
url = "https://pump.fun/advanced"  # Replace with your target URL

# Set up Selenium WebDriver for Firefox
service = Service(webdriver_path)
driver = webdriver.Firefox(service=service)

# Open the webpage in the browser
driver.get(url)

print(f"Monitoring {url} for <tr data-index> elements...\n")

seen_mints = set()

directory = "data"

if len(sys.argv) < 2:
    print("Usage: python script.py <directory>")
else:     
    directory = sys.argv[1]


def fire_and_forget_print(*args):
    print_data(*args)

     
def parse_mint(mint_url):
    return mint_url.strip('/').split('/')[-1]

# Function to parse the user URL
def parse_user(user_url):
    return user_url.strip('/').split('/')[-1]

# Function to parse the image URL
def parse_img(img_url):
    item =  img_url.strip('/').split('/')[-1]
    item =  item.split('?')[0]
    # Parse the URL to remove query parameters
    return item
def login_and_create_session(username, password):
    session = requests.Session()

    # Headers with User-Agent and Referer
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Referer': 'https://gamebackrooms.com/login/',  # Replace with the login URL
    }

    # Login data
    login_data = {
        'username': username,
        'password': password,
    }

    try:
        # Step 1: Fetch CSRF token from the login page
        login_url = 'https://gamebackrooms.com/login/'
        response = session.get(login_url, headers=headers)

        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            csrf_token = soup.find('input', {'name': 'csrfmiddlewaretoken'})['value']

            # Step 2: Prepare login data with CSRF token included
            login_data['csrfmiddlewaretoken'] = csrf_token

            # Step 3: Login request with headers and Referer set
            login_response = session.post(login_url, data=login_data, headers=headers)

            # Check if login was successful
            if login_response.status_code == 200:
                print('Login successful!')
                return session
            else:
                print(f'Login failed with status code {login_response.status_code}')
                print(login_response.text)  # Print error message or response content
                return None

        else:
            print(f'Failed to fetch CSRF token, status code: {response.status_code}')
            print(response.text)  # Print error message or response content
            return None

    except requests.RequestException as e:
        print(f'An error occurred during login: {e}')
        return None


def print_data(ticker, name, mint, user, img_url):

    print(mint)
    print(name)    
    print(ticker)
    print(user)
    
    print(img_url)

    img_hash = parse_img(img_url)
    new_img_url = f'https://ipfs.io/ipfs/{img_hash}'

    # Data dictionary
    mint = parse_mint(mint)

    if mint:


        session = login_and_create_session(username, password)

        analysis_content = name + " $" + ticker + " CA: " + mint 

        payload_to_send = {}

        payload_to_send["name"] = name
        payload_to_send["symbol"] = ticker
        payload_to_send["image_uri"] = new_img_url
        payload_to_send["ai_analysis"] = analysis_content
        payload_to_send["creator"] = user
        

        # Add 'mint' key-value pair
        payload_to_send['mint'] = mint

        # Login session                        
        url_prod = 'https://gamebackrooms.com/create_token/'


        # Send the payload 
        try:
            response = session.post(url_prod, data=payload_to_send)
            print(response)

            print("Response status:", response.status_code)
            print("Response content:", response.text)

        except Exception as e:
            print(f"An error occurred: {e}")


        data = {
            "signature": mint,
            "name": name,
            "symbol": ticker,
            "image_url": new_img_url,
            "user": user
        }

        '''
        generated_uuid = str(uuid.uuid4()) 
        txt_file_path = os.path.join(directory, f"{generated_uuid}.{mint}.txt")
        json_file_path = os.path.join(directory, f"{generated_uuid}.{mint}.json")
    

        # Save data to JSON file
        with open(txt_file_path, "w") as txt_file:
            json.dump(data, txt_file, indent=4)
            time.sleep(1)
    

        while not os.path.exists(txt_file_path):
            print(f"{txt_file_path} does not exist. Retrying in 1 second...")
            time.sleep(2)  # Wait for 1 second before checking again

        # When the file exists, rename it
        os.rename(txt_file_path, json_file_path)
        '''
                        

try:
    while True:
        # Fetch all <tr> elements with the attribute 'data-index'
        elements = driver.find_elements(By.CSS_SELECTOR, "tr[data-index]")

        extracted_data = []  # List to hold all extracted rows' data

        # Process each <tr> element
        if elements:
            print("Matching <tr data-index> elements found:")
            for element in elements:
                try:
                    hasProfile = False

                    # Prepare local copies for each row
                    row_data = {
                        "ticker": "",
                        "name": "",
                        "mint": "",
                        "user": "",
                        "links": [],
                        "images": [],
                        "profile_image": ""
                    }

                    # Extract text content
                    lines = element.text.split("\n")
                    if len(lines) >= 2:  # Ensure there are at least two lines
                        row_data["ticker"] = lines[0]
                        row_data["name"] = lines[1]

                    # Extract links
                    links = element.find_elements(By.TAG_NAME, "a")
                    for link in links:
                        try:
                            href = link.get_attribute('href')
                            text = link.text
                            row_data["links"].append({'text': text, 'href': href})
                        except Exception as e:
                            print(f"Error accessing link text or href: {e}")

                    # Extract images
                    images = element.find_elements(By.TAG_NAME, "img")
                    for img in images:
                        try:
                            src = img.get_attribute('src')
                            alt = img.get_attribute('alt')
                            row_data["images"].append({'src': src, 'alt': alt})

                            # Check for profile image condition
                            if src and src.startswith("https://pump.mypinata.cloud"):
                                row_data["profile_image"] = src
                                hasProfile = True
                        except Exception as e:
                            print(f"Error accessing image src or alt: {e}")

                    # Process link data for specific fields
                    if row_data["links"]:
                        row_data["mint"] = row_data["links"][0]['href'] if len(row_data["links"]) > 0 else ''
                        row_data["user"] = row_data["links"][1]['href'] if len(row_data["links"]) > 1 else ''

                    # Add extracted row data to the list
                    if hasProfile:
                        extracted_data.append(row_data)

                except Exception as e:
                    print(f"Error accessing content in <tr>: {e}")

            # Print extracted data
            for data in extracted_data:
                print(f"Ticker: {data['ticker']}")
                print(f"Name: {data['name']}")
                print(f"Mint: {data['mint']}")
                print(f"User: {data['user']}")
                print(f"Profile Image: {data['profile_image']}")
                #print(f"Links: {data['links'][0]['href']}")
                print(f"Images: {data['images'][0]['src']}")
                print("-" * 50)
                if data['user']:
                    thread = threading.Thread(target=fire_and_forget_print, args=(data['ticker'], data['name'], data['mint'], parse_user(data['user']), data['images'][0]['src']))
                    thread.start()                    
                    print_data(data['ticker'], data['name'], data['mint'], data['user'], data['images'][0]['src'])
                else:
                    generated_uuid = str(uuid.uuid4()) 
                    thread = threading.Thread(target=fire_and_forget_print, args=(data['ticker'], data['name'], data['mint'], generated_uuid, data['images'][0]['src']))
                    thread.start()                    

        else:
            print("No <tr data-index> elements found.")

        # Wait before the next check (adjust the interval as needed)
        time.sleep(5)

except KeyboardInterrupt:
    print("Stopped by user.")

finally:
    # Close the browser when done
    driver.quit()
