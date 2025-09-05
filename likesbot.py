import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import threading
import re

# Replace with your bot's access token
TELEGRAM_TOKEN = "7600964444:AAG8RN8Qa18ODkBByl_for9ScdEZWYJrPyY"
received_url = None
chrome_driver_path = r"C:\selenium\chromedriver-win64\chromedriver-win64\chromedriver.exe"
options = Options()
service = Service(chrome_driver_path)

accounts = [
    {'email': 'evamillexo', 'username': 'evamillerxo', 'password': 'krish@6969'},
    # Add more accounts...
]
def login_and_like(account,url):
    # Path to ChromeDriver
    # chrome_driver_path = r"C:\selenium\chromedriver-win64\chromedriver.exe"

    # Setup Chrome options for using proxy
    
    # options.add_argument(f'--proxy-server={account["proxy"]}')

    # Start the Chrome browser with the proxy
    # service = Service(chrome_driver_path)
     #, options=options service=service
    options = Options()
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(service=service,options=options)

    try:
        # Open Twitter login page
        driver.get("https://twitter.com/login")
        time.sleep(random.uniform(15,20))  # Random delay to mimic human interaction

        # Log in to the account
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'text'))
        )
        username_input.send_keys(account['email'])

        # Click 'Next' button
        next_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Next']"))
            
        )
        print("next button found")
        next_button.click()

        try:
            # Handle unusual activity input if present
            unusual_activity_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            unusual_activity_input.send_keys(account['username'])  # Assuming same username is asked

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
        password_input.send_keys(account['password'])

        # Click 'Log In' button
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
        )
        login_button.click()

        # Wait for the login to complete
        WebDriverWait(driver, 20).until(
            EC.url_changes("https://twitter.com/login")
        )

        time.sleep(10)  # Wait for login to complete

        # Navigate to the reply and like it (update with your reply URL)
        driver.get(url)  # Replace with the actual reply URL

        time.sleep(random.uniform(4,6))
        # filter_latest_comments()                       # Wait for page load
        try:
            driver.execute_script(f"window.scrollBy(0, {550});")
            
            like_buttons = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'id__')]/div[3]/button/div/div[1]/div")

            print(f"Found {len(like_buttons)} potential like buttons.")

            # Get the first two like buttons only
            for like_button in like_buttons[:2]:
                try:
                    color = like_button.value_of_css_property("color")
                    print(color)

                    if color == "rgba(249, 24, 128, 1)":
                        print("Already liked")
                    else:
                        print("Liking")
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
                    print("No comments yet")

        except TimeoutException:
            print("Like buttons not found or not clickable.")
        except NoSuchElementException:
            print("No comments yet")

        time.sleep(random.uniform(2, 4))  # Wait after liking

    except TimeoutException:
        print("Login failed or an element could not be located in time.")
    finally:
        driver.quit()
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Send me the URL to open with the bot!')

processing = False  # Flag to prevent processing multiple URLs at the same time

# Function to validate URL format
def is_valid_url(url):
    url_pattern = re.compile(
        r'^(https?://)?(www\.)?x\.com/[a-zA-Z0-9_]+(/.*)?$'
    )
    return bool(url_pattern.match(url))

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global received_url, processing
    if processing:
        await update.message.reply_text(
            "I'm still processing the previous URL. Please wait."
        )
        return

    received_url = update.message.text

    # Validate URL format
    if not is_valid_url(received_url):
        await update.message.reply_text(
            "Invalid URL format! Please send a valid URL in the format: https://x.com/username/with_replies"
        )
        return

    await update.message.reply_text(f'URL received: {received_url}')
    processing = True  # Set the flag to indicate a process is running

    # Start threads for each account
    threads = []
    for account in accounts:
        thread = threading.Thread(target=login_and_like, args=(account, received_url))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    await update.message.reply_text("Processing completed for the URL!")
    processing = False  # Reset the flag
    

def main():
    # Create the Application instance
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url))

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    main()


# Proxy list and account info (use secure storage for credentials)


# def smooth_scroll(y_offset, step=5, duration=0.01):
#     """
#     Smoothly scrolls the page by the specified y_offset.
#     :param y_offset: Total amount of pixels to scroll vertically.
#     :param step: Pixels to scroll per iteration (smaller values mean smoother scrolling).
#     :param duration: Delay between scroll steps (in seconds).
#     """
#     current_position = driver.execute_script("return window.pageYOffset;")
#     target_position = current_position + y_offset
#     scroll_direction = 1 if y_offset > 0 else -1
    
#     while abs(target_position - current_position) > step:
#         current_position += step * scroll_direction
#         driver.execute_script(f"window.scrollTo(0, {current_position});")
#         time.sleep(duration)

#     # Final scroll to the exact target position (to prevent overshooting)
#     driver.execute_script(f"window.scrollTo(0, {target_position});")
# def filter_latest_comments():
    
#     try:
#         smooth_scroll(1400,10,0.01)
#         time.sleep(4)
#         # Locate and click the filter button to open dropdown
#         filter_button_xpath = '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div/div[3]/div/button[2]/div'
#         filter_button = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, filter_button_xpath))
#         )
#         filter_button.click()
#         time.sleep(2)

#         # Locate and click the "Latest" option in the dropdown
#         latest_option_xpath = '//span[text()="Latest"]/ancestor::div[@role="menuitem"]'
#         latest_option = WebDriverWait(driver, 10).until(
#             EC.element_to_be_clickable((By.XPATH, latest_option_xpath))
#         )
#         latest_option.click()
#         time.sleep(2)
#         print("Filtered by latest comments.")

#     except TimeoutException:
#         print("Could not locate the filter button or 'Latest' option.")
#     except NoSuchElementException:
#         print("No filter button or 'Latest' option found on the page.")
# Function to log in with proxy and like a reply
  # Always close the browser

# Loop through accounts
# for account in accounts:
#     login_and_like(account)
#     time.sleep(random.uniform(30, 60))  # Delay between account actions
