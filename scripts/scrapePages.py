# SCRAPING LINKS FOR DATA WITH SELENIUM + WEBDRIVER

# Import necessary libraries
from selenium import webdriver  # Import Selenium webdriver for web automation
from selenium.webdriver.common.keys import Keys  # Import Keys for keyboard actions
from selenium.webdriver.chrome.service import Service  # Import Chrome service for Selenium
from webdriver_manager.chrome import ChromeDriverManager  # Import ChromeDriverManager for managing ChromeDriver
from selenium.webdriver.common.by import By  # Import By for locating elements
from selenium.webdriver.support.ui import WebDriverWait  # Import WebDriverWait for waiting for elements
from selenium.webdriver.support import expected_conditions as EC  # Import expected_conditions for specifying conditions
import pandas as pd  # Import Pandas library for data manipulation
import os  # Import os for operating system functions
import re  # Import re library for regular expressions
import time  # Import time for time-related functions

# Set the path to the ChromeDriver executable (replace with your own path)
import constants
chrome_path = constants.CHROME_WEBDRIVER
os.chmod(chrome_path, 0o700)  # Change file permissions to allow execution

# Create a ChromeDriver service with the specified path
chrome_service = webdriver.chrome.service.Service(chrome_path)
driver = webdriver.Chrome(service=chrome_service)  # Start a new Chrome WebDriver instance
df = pd.read_csv('GoFundMe-Weblinks.csv')  # Read the CSV file containing links

# Regular expression pattern to extract valid GoFundMe URLs
pattern = r"https://www\.gofundme\.com/f/.*?(?=[?/])"
extraction = []
counter = 100

# Iterate over each row in the DataFrame to scrape data from GoFundMe campaign pages
for index, row in df.iterrows():
    counter -= 1
    if counter == 0:
        counter = 100
        time.sleep(400)  # Sleep for 400 seconds (rate limiting)
        os.chmod(chrome_path, 0o700)  # Update file permissions
        chrome_service = webdriver.chrome.service.Service(chrome_path)
        driver = webdriver.Chrome(service=chrome_service)

    if 'www.gofundme.com/f/' in row['Link']:
        url = row['Link'] + "/"
        match = re.search(pattern, url)  # Match the URL against the pattern
        if match:
            link = match.group(0)
            driver.get(link)  # Open the GoFundMe campaign page

            # Extract campaign details using Selenium and XPath selectors
            # Extract title
            try:
                title_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//h1[@class="hrt-mb-0 p-campaign-title"]')))
                title = title_element.text  # Get the campaign title
            except:
                title = ""
            
            # Extract location
            try:
                location_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="hrt-text-body-sm"]')))
                location = location_element[1].text  # Get the campaign location
            except:
                location = ""

            # Extract amount raised and goal
            raised_goal_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="progress-meter_progressMeterHeading__A6Slt"]')))
            
            # Extract description of fundraiser
            description_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@class="campaign-description_campaignDescription__6P_RU"]')))

            # Create a dictionary containing extracted data
            data = {'title': [title], 'raised_goal': [raised_goal_element.text],
                    'description': [description_element.text], 'location': [location]}
            df = pd.DataFrame(data)  # Create a DataFrame from the extracted data

            # Append the DataFrame to a CSV file
            df.to_csv('GoFundMe-Data.csv', mode='a', index=False, header=False)

driver.close()  # Close the Chrome WebDriver instance
