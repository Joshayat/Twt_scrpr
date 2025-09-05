import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException


driver = webdriver.Chrome()
driver.get("https://x.com/login")
time.sleep(3)
username_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, 'text'))
)
username_input.send_keys("evamillerxo")

# Click 'Next' button
next_button = WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Next']"))
)
next_button.click()

try:
    unusual_activity_input = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.NAME, "text"))
    )
    unusual_activity_input.send_keys("Babymartxxx")

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
password_input.send_keys("krish@6969")

# Click 'Log In' button
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
)
login_button.click()


post_links = []

def scrape_post_urls(profile_url):
    driver.get(profile_url)
    
    # Wait for the page to load and ensure the first tweet is present
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))
        )
        print("Page loaded, scraping the first two posts.")
    except TimeoutException:
        print("Page took too long to load.")
        return []

    driver.execute_script("window.scrollBy(0, 550);")

    # Scrape the first post
    try:
        first_post = driver.find_element(By.XPATH, '//article[@data-testid="tweet"]')
        link = first_post.find_element(By.XPATH, './/time/parent::a')
        post_links.append(link.get_attribute('href'))
        print("First post URL:", link.get_attribute('href'))
    except NoSuchElementException:
        print("First post not found or link not available.")

    # Scroll to load the second post
   
    time.sleep(2)  # Give time for the second post to load

    # Scrape the second post
    try:
        second_post = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')[1]  # Get the second post
        link = second_post.find_element(By.XPATH, './/time/parent::a')
        post_links.append(link.get_attribute('href'))
        print("Second post URL:", link.get_attribute('href'))
    except (NoSuchElementException, IndexError):
        print("Second post not found or link not available.")

    return post_links

# Example usage
post_links = scrape_post_urls("https://x.com/babymartxxx")
print(post_links)

time.sleep(10)
