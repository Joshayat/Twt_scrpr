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
def filter_latest_comments():
    try:
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
# Function to interact with like buttons
def like_posts():
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
                    time.sleep(0.5)
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
        
        
# def monitor_comments_for_post(post_url):
#     driver.get(post_url)
#     time.sleep(5)
#     while True:
#         print("Checking for new comments...")
#         like_posts()
#         wait_time = random.randint(600, 900)  # 10-15 minutes
#         print(f"Waiting for {wait_time / 60:.2f} minutes before next check.")
#         time.sleep(wait_time)
# start_time = time.time()
# while time.time() - start_time < 24 * 60 * 60:  # Run for 24 hours
#     # Scrape new posts every 6 hours
#     post_links = scrape_post_urls("https://x.com/babymartxxx")
#     print(f"Scraped posts: {post_links}")

#     # Monitor comments for each post
#     for post_link in post_links:
#         monitor_comments_for_post(post_link)

#     print("Waiting 6 hours to check for new posts.")
#     time.sleep(6 * 60 * 60)
