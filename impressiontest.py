import time
from datetime import datetime, timezone, timedelta
import random

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException, StaleElementReferenceException

# Setup Chrome WebDriver
import asyncio
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext,Application,ContextTypes

# Telegram Bot Token
TELEGRAM_API_TOKEN = "7598394273:AAEv-PShPLKbYj8BoPKCD9Z3xQWYNPomMgc"

# Store chat IDs in memory (use a database or file for persistence if needed)
registered_users = {1981206622, 5311708356,5863505513}
application = None
#chrome_driver_path = r"C:\selenium\chromedriver-win64\chromedriver-win64\chromedriver.exe"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handle the /start command. Registers the user's chat ID.
    """
    chat_id = update.effective_chat.id
    if chat_id in registered_users:
        await update.message.reply_text("You are already registered for alerts.")
    else:
        await update.message.reply_text("Sorry, you are not authorized to receive alerts.")

async def send_alert_to_users(message: str):
    """
    Send an alert to all registered users.
    """
    global application
    for chat_id in registered_users:
        try:
            await application.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")
# def initialize_chrome():
#     """
#     Initialize the Selenium Chrome WebDriver.
#     """
#     options = Options()
#     #options.add_argument("--start-maximized")
#     service = Service(chrome_driver_path)
#     return webdriver.Chrome(service=service, options=options)
def login_to_twitter(driver):
    """
    Perform login to Twitter.
    """
    driver.get("https://x.com/login")
    time.sleep(3)

    # Enter username
    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, 'text'))
    )
    username_input.send_keys("suii37333@gmail.com")

    # Click 'Next' button
    next_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Next']"))
    )
    next_button.click()

    # Handle unusual activity, if needed
    try:
        unusual_activity_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        unusual_activity_input.send_keys("vrax6969")
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/ancestor::button"))
        )
        next_button.click()
    except TimeoutException:
        print("No unusual activity page detected.")

    # Enter password
    password_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys("Vrax@1234")

    # Click 'Log In' button
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
    )
    login_button.click()

    # Wait for login to complete
    WebDriverWait(driver, 20).until(EC.url_changes("https://x.com/login"))
    print("login done")
    time.sleep(10)
def scroll_and_collect_replies(driver,processed_urls,filtered_reply_links):
   
    
    scroll_count=3
    for _ in range(scroll_count):
        current_time = datetime.now(timezone.utc) 
        # Scroll down to load more replies
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(5)  # Allow replies to load

        # Collect replies on the current scroll
        new_replies = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
        )

        for reply in new_replies:
            try:
                # driver.execute_script("arguments[0].scrollIntoView(true);", reply)
                time.sleep(3)

                # Extract reply URL
                url = reply.find_element(By.XPATH, './/time/parent::a').get_attribute('href')
                if url in processed_urls or url in filtered_reply_links:
                    continue  # Skip if URL is already processed
                # print(f"url is {url}")

                # Extract post time
                time_text = reply.find_element(By.XPATH, './/time').get_attribute("datetime")
                post_time = datetime.fromisoformat(time_text.replace("Z", "+00:00"))
                time_only = post_time.time() 
                # formatted_time = post_time.strftime("%H:%M:%S")
                # print(formatted_time) 
                # print(f"time is {time_only}")
                # print(f"current time {current_time}")
                minutes_since_posted = (current_time - post_time).total_seconds() / 60
                # print(minutes_since_posted)

                # Extract impressions text and calculate impressions
                impressions_element = reply.find_element(By.XPATH, ".//div[contains(@id, 'id__')]/div[4]/a/div/div[2]/span/span/span")
                impressions_text = impressions_element.text
                if 'K' in impressions_text:
                    impressions_count = float(impressions_text.replace('K', '').strip()) * 1000
                elif 'M' in impressions_text:
                    impressions_count = float(impressions_text.replace('M', '').strip()) * 1000000
                else:
                    impressions_count = int(impressions_text)
                
                print(f"Impressions: {impressions_count}")
                postImpression_ratio=impressions_count/minutes_since_posted if minutes_since_posted > 0 else 0
                if minutes_since_posted <= 300 and postImpression_ratio > 50:
                    filtered_reply_links.add(url)
                    alert_message = (
                        f"🚨 *New Reply Alert!*\n\n"
                        f"🔗 [Click to view reply]({url})\n"
                        f"📊 *Impressions-to-Minutes Ratio:* {postImpression_ratio:.2f}\n"
                        f"⏱ *Minutes since posted:* {minutes_since_posted:.2f}"
                    )
                    asyncio.run(send_alert_to_users(alert_message))
                
                # Add URL to processed URLs to avoid reprocessing
                processed_urls.add(url)

            except StaleElementReferenceException:
                print("Encountered StaleElementReferenceException for a reply, skipping.")
                
    print(f"Collected {len(processed_urls)} unique replies.")
    return processed_urls
         # Add to set to avoid duplicates



# Set to store URLs that meet the conditions


    # Display desktop notification
def alert_new_filtered_link(url, ratio, minutes_since_posted):
    """
    Sends a Telegram alert when a new reply is filtered.
    """
    alert_message = (
        f"🚨 *New Reply Alert!*\n\n"
        f"🔗 [Click to view reply]({url})\n"
        f"📊 *Impressions-to-Minutes Ratio:* {ratio:.2f}\n"
        f"⏱ *Minutes since posted:* {minutes_since_posted:.2f}"
    )
    send_alert_to_users(alert_message,application)







def run_scraper():
    """
    Initialize Chrome and run the scraping loop.
    """
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    login_to_twitter(driver)

    processed_urls = set()
    filtered_reply_links = set()

    while True:
        current_time = datetime.now()
        if (current_time - last_reset_time).total_seconds() >= 7200:  # 7200 seconds = 2 hours
            print("Resetting processed and filtered URL sets...")
            processed_urls.clear()
            filtered_reply_links.clear()
            last_reset_time = current_time
        driver.get("https://x.com/realonx1/with_replies")
        time.sleep(5)

        # Scroll and collect replies
        scroll_and_collect_replies(driver, processed_urls, filtered_reply_links)

        # Wait before refreshing
        next_refresh = random.randint(20, 25)
        print(f"Waiting {next_refresh} minutes before the next refresh.")
        time.sleep(next_refresh * 60)
def main():
    """
    Run the Telegram bot and scraper concurrently.
    """
    global application
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    # Run the bot and scraper concurrently
    print("Starting Telegram bot and scraper...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_in_executor(None, run_scraper)
    application.run_polling()


if __name__ == "__main__":
    main()