import time
from datetime import datetime, timezone, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException,TimeoutException

# Initial setup
chrome_driver_path = r"C:\selenium\chromedriver-win64\chromedriver-win64\chromedriver.exe"
options = Options()
service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get("https://x.com/login")
time.sleep(3)

user_name = "latestjoboffers7@gmail.com"
pass_word = "krish@6969"

# Login code here (omitted for brevity)

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
password_input = WebDriverWait(driver, 15).until(
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
time.sleep(5)
driver.get("https://x.com/realonx1/with_replies")

processed_urls = set()
scroll_count = 3
reply_elements = set()

def checker(reply, processed_urls):
    try:
        # Refetch the reply element to avoid stale reference issues
        url = reply.find_element(By.XPATH, './/time/parent::a').get_attribute('href')
        if url in processed_urls:
            return None  # Skip if already processed

        # Get post time
        time_text = reply.find_element(By.XPATH, './/time').get_attribute("datetime")
        post_time = datetime.fromisoformat(time_text.replace("Z", "+00:00"))
        
        # Get impressions
        impressions_element = reply.find_element(By.XPATH, ".//div[contains(@id, 'id__')]/div[4]/a/div/div[2]/span/span/span")
        impressions_text = impressions_element.text
        if 'K' in impressions_text:
             impressions_count = float(impressions_text.replace('K', '').strip()) * 1000
        elif 'M' in impressions_text:
            impressions_count = float(impressions_text.replace('M', '').strip()) * 1000000
        else:
            impressions_count = int(impressions_text) 
        print(impressions_count)
        
        processed_urls.add(url)
        return url, post_time, impressions_count

    except StaleElementReferenceException:
        print("Skipped due to stale reference")
        return None

# Smooth scroll and collect replies
for _ in range(scroll_count):
    driver.execute_script("window.scrollBy(0, 650);")
    time.sleep(3)  # Let replies load

    replies = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
    )

    for reply in replies:
        result = checker(reply, processed_urls)
        if result:
            url, post_time, impressions_count = result
            print(f"url: {url}, time: {post_time}, impressions: {impressions_count}")

print(f"Processed {len(processed_urls)} replies.")
driver.quit()
