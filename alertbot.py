import time
from datetime import datetime, timezone, timedelta
import random
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException

# Setup Chrome WebDriver
chrome_driver_path = r"C:\selenium\chromedriver-win64\chromedriver-win64\chromedriver.exe"
options = Options()
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://x.com/login")
time.sleep(3)

user_name = "latestjoboffers7@gmail.com"
pass_word = "krish@6969"

# Enter username
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://x.com/login")
username_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, 'text'))
)
username_input.send_keys("Vrax69699")

# Click 'Next' button
next_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Next']"))
)
next_button.click()

try:
    unusual_activity_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    unusual_activity_input.send_keys("Vrax69699")

    next_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/ancestor::button"))
    )
    next_button.click()

except TimeoutException:
    print("No unusual activity page detected, continuing with the login process.")

# Enter password
password_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'password'))
)
password_input.send_keys("Vrax@1234")

# Click 'Log In' button
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
)
login_button.click()

# Wait for the login to complete
WebDriverWait(driver, 20).until(
    EC.url_changes("https://x.com/login")
)
driver.get("https://x.com/realonx1/with_replies")
time.sleep(15)
driver.execute_script(f"window.scrollBy(0, {600});")
time_limit = timedelta(hours=4)
impressions_threshold_per_minute = 25
all_reply_links = set()
scroll_count = 5

# Scroll and collect replies within the time limit and impression threshold
for _ in range(scroll_count):
    driver.execute_script(f"window.scrollBy(0, {600});")
    time.sleep(5)  # Allow new replies to load

    reply_elements = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
    )[:10]  # Adjust the range as needed

    # Collect URLs of replies that meet the time and impression requirements
    for link in reply_elements:
        try:
            # Extract reply URL
            url = link.find_element(By.XPATH, './/time/parent::a').get_attribute('href')
            print(url)
            
            # Extract time and filter based on 4-hour limit
            time_text = link.find_element(By.XPATH, './/time').get_attribute("datetime")
            post_time = datetime.fromisoformat(time_text.replace("Z", "+00:00"))
            current_time = datetime.now(timezone.utc)
            print(post_time)
            
            # Calculate if within 4 hours
            # within_time_limit = (current_time - post_time) <= time_limit

            # Extract impressions text and calculate impressions per minute
            impressions_element = link.find_element(By.XPATH, "//div[contains(@id, 'id__')]/div[4]/a/div/div[2]/span/span/span")
            impressions_text = impressions_element.text
            print(f"text is {impressions_text}")
            if 'K' in impressions_text:
                
                impressions_count = float(impressions_text.replace('K', '').strip()) * 1000
            elif 'M' in impressions_text:
                impressions_count = float(impressions_text.replace('M', '').strip()) * 1000000
            else:
                impressions_count = int(impressions_text) 
            print(impressions_count)
            # minutes_since_posted = (current_time - post_time).total_seconds() / 60
            # impressions_per_minute = impressions_count / minutes_since_posted if minutes_since_posted > 0 else 0
           

            # # Check if impressions meet threshold and add URL if both conditions are met
            # if within_time_limit and impressions_per_minute > impressions_threshold_per_minute:
            #     all_reply_links.add(url)
          
        except Exception as e:
            
            print(f"Skipped due to error: {e}")
            continue

# Print collected reply URLs
for url in all_reply_links:
    print(url)

# Close the driver when done
driver.quit()

