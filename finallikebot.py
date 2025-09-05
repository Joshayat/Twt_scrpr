import time
import random
from datetime import datetime, timedelta
from datetime import datetime
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
    unusual_activity_input.send_keys("evamillerxo")

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
WebDriverWait(driver, 20).until(
    EC.url_changes("https://x.com/login")
)
time.sleep(10)

post_links = []
def scrape_latest_post(profile_url):
    driver.get(profile_url)
    time.sleep(5)
    
    # Wait for the page to load and ensure the first tweet is present
    try:
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))
        )
        print("Page loaded, scraping the first two posts.")
    except TimeoutException:
        print("Page took too long to load.")
        return None

    driver.execute_script("window.scrollBy(0, 550);")
    time.sleep(5)

    posts = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
    
    latest_post_url = None
    latest_post_time = None

    # Loop through the first two posts and check timestamps
    for i, post in enumerate(posts[:2]):
        try:
            # Extract the post link
            link = post.find_element(By.XPATH, './/time/parent::a')
            post_url = link.get_attribute('href')
            
            # Extract and parse the post timestamp
            timestamp = post.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
            post_time = datetime.fromisoformat(timestamp[:-1])  # Remove 'Z' if present for UTC
            
            print(f"Post {i + 1} URL: {post_url}")
            print(f"Post {i + 1} Timestamp: {post_time}")
            
            # Determine the latest post by comparing timestamps
            if latest_post_time is None or post_time > latest_post_time:
                latest_post_time = post_time
                latest_post_url = post_url

        except NoSuchElementException:
            print(f"Post {i + 1} not found or link not available.")
            continue

    return latest_post_url

latest_post_link = scrape_latest_post("https://x.com/babymartxxx")
print("Latest post URL:", latest_post_link)
def smooth_scroll(y_offset, step=5, duration=0.01):
    """
    Smoothly scrolls the page by the specified y_offset.
    :param y_offset: Total amount of pixels to scroll vertically.
    :param step: Pixels to scroll per iteration (smaller values mean smoother scrolling).
    :param duration: Delay between scroll steps (in seconds).
    """
    current_position = driver.execute_script("return window.pageYOffset;")
    target_position = current_position + y_offset
    scroll_direction = 1 if y_offset > 0 else -1
    
    while abs(target_position - current_position) > step:
        current_position += step * scroll_direction
        driver.execute_script(f"window.scrollTo(0, {current_position});")
        time.sleep(duration)

    # Final scroll to the exact target position (to prevent overshooting)
    driver.execute_script(f"window.scrollTo(0, {target_position});")
def filter_latest_comments():
    
    try:
        smooth_scroll(1400,10,0.01)
        time.sleep(4)
        # Locate and click the filter button to open dropdown
        filter_button_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/button[2]/div'
        filter_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, filter_button_xpath))
        )
        filter_button.click()
        time.sleep(2)

        # Locate and click the "Latest" option in the dropdown
        latest_option_xpath = '//span[text()="Latest"]/ancestor::div[@role="menuitem"]'
        latest_option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, latest_option_xpath))
        )
        latest_option.click()
        time.sleep(2)
        print("Filtered by latest comments.")

    except TimeoutException:
        print("Could not locate the filter button or 'Latest' option.")
    except NoSuchElementException:
        print("No filter button or 'Latest' option found on the page.")
def like_posts(latest_post_link):
    
    driver.get(latest_post_link)
    # First, filter by latest comments
    filter_latest_comments()

    try:
        # Find all potential like buttons and limit to the first 10
        like_buttons = driver.find_elements(By.XPATH, "//div[@id][contains(@id, 'id__')]/div[3]/button/div/div[1]/div")[:10]
        print(f"Found {len(like_buttons)} potential like buttons.")

        for like_button in like_buttons:
            try:
                color = like_button.value_of_css_property("color")
                print(f"Like button color: {color}")

                if color == "rgba(249, 24, 128, 1)":
                    print("Already liked")
                else:
                    print("Liking post")
                    driver.execute_script("arguments[0].scrollIntoView(true);", like_button)
                    time.sleep(1)
                    driver.execute_script("arguments[0].click();", like_button)
                    time.sleep(2)

            except ElementClickInterceptedException:
                color = like_button.value_of_css_property("color")
                if color != "rgba(249, 24, 128, 1)":
                    driver.execute_script("arguments[0].scrollIntoView(true);", like_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", like_button)
                    time.sleep(2)
            except NoSuchElementException:
                print("No like button found.")

    except TimeoutException:
        print("Like buttons not found or not clickable.")
    except NoSuchElementException:
        print("No comments or like buttons found.")
def main():
    profile_url = "https://x.com/babymartxxx"
    latest_post_link = scrape_latest_post(profile_url)
    print("Initial latest post URL:", latest_post_link)

    next_post_check_time = datetime.now() + timedelta(hours=10)
    next_like_check_time = datetime.now()

    while True:
        current_time = datetime.now()

        if current_time >= next_post_check_time:
            print("Checking for a new post...")
            new_post_link = scrape_latest_post(profile_url)
            
            if new_post_link and new_post_link != latest_post_link:
                latest_post_link = new_post_link
                print("New post detected! Updated latest post URL:", latest_post_link)
            
            next_post_check_time = current_time + timedelta(hours=10)

        if latest_post_link and current_time >= next_like_check_time:
            print("Refreshing post link to check for new comments...")
            driver.get(latest_post_link)
            like_posts(latest_post_link)
            
            next_like_interval = random.choice([10, 15, 20])
            next_like_check_time = current_time + timedelta(minutes=next_like_interval)
            print(f"Next comment check in {next_like_interval} minutes.")

        time.sleep(5)

# Run the main loop
main()