import time
import random
from selenium import webdriver
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

options.add_argument("--window-size=800,600")
options.add_argument("--headless")  # Keep the browser in headless mode so it runs in the background

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service, options=options)

# Log in to X (Twitter)
driver.get("https://x.com/login")
time.sleep(3)

user_name = "latestjoboffers7@gmail.com"
pass_word = "Krish@6969"

# Enter username
username_input = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.NAME, 'text'))
)
username_input.send_keys(user_name)

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
password_input.send_keys(pass_word)

# Click 'Log In' button
login_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
)
login_button.click()

# Wait for the login to complete
WebDriverWait(driver, 20).until(
    EC.url_changes("https://x.com/login")
)

print("Logged in successfully!")
time.sleep(5)

# Navigate to profile and post
profile_url = "https://x.com/Babymartxxx"
driver.get("https://x.com/babymartxxx/status/1826196861037732255")
time.sleep(20)
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

# Main loop to refresh the page every 10-15 minutes for 12 hours
start_time = time.time()
twelve_hours = 12 * 60 * 60  # 12 hours in seconds

while time.time() - start_time < twelve_hours:
    like_posts()

    # Random wait time between 10 and 15 minutes
    wait_time = random.randint(600, 900)
    print(f"Waiting for {wait_time / 60:.2f} minutes before refreshing.")
    time.sleep(wait_time)

    # Refresh the page
    driver.refresh()
    time.sleep(5)  # Give time for the page to reload



"""//*[@id="id__gwflyy8c65"]/div[3]/button/div/div[1]/svg"""


# Function to scrape post URLs from the profile
"""def scrape_post_urls(profile_url, num_posts):
    driver.get(profile_url)
    time.sleep(3)  # Wait for the page to load

    post_links = []
    last_height = driver.execute_script("return document.body.scrollHeight")

    while len(post_links) < num_posts:
        # Find all posts on the profile page
        posts = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')
        for post in posts:
            if len(post_links) >= num_posts:
                break  # Stop collecting if we have enough posts
            
            try:
                link = post.find_element(By.XPATH, './/time/parent::a')
                post_links.append(link.get_attribute('href'))
            except NoSuchElementException:
                continue  # Skip if the link is not found

        # Scroll down to load more posts if we haven't reached the desired number
        if len(post_links) < num_posts:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for new posts to load

            # Check if we've reached the bottom
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                print("Reached the bottom of the page, no more new posts.")
                break
            last_height = new_height

    return post_links[:num_posts]  # Return only the specified number of posts

# Example usage:
profile_url = "https://x.com/username"
post_links = scrape_post_urls(profile_url, 2)  # Get the first 2 posts
print(post_links)
"""

# Get post URLs from the profile
 # Replace with your actual username
"""post_urls = scrape_post_urls(profile_url)"""

"""print("Post URLs:", post_urls)

# Set a time limit (in seconds)
time_limit = 300  # Example: 5 minutes
start_time = time.time()"""

# Infinite loop until the time limit is reached

          # Exit the while loop if time is up



# Infinite loop to keep checking for new comments

"""while True:
    check_and_like_comments()
    driver.refresh()
    print("Page refreshed, checking for new comments...")
    time.sleep(200)  # Adjust delay"""
  
"""comments = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="reply"]')
print(comments)

for comment in comments:
    comment_id = comment.get_attribute("data-testid")
    
    # Skip if the comment has already been liked
    if comment_id in liked_comments:
        continue

    try:
        # Like each comment
        like_button = comment.find_element(By.XPATH, './/div[@data-testid="like"]//svg')
        like_button.click()
        print(f"Liked comment with ID: {comment_id}")

        # Add the comment's ID to the set of liked comments
        liked_comments.add(comment_id)

        time.sleep(1)  # Small delay to avoid being flagged
    except Exception as e:
        print(f"Error while liking comment {comment_id}: {e}")
        continue"""
        