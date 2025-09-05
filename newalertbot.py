import time
from datetime import datetime, timezone
import random
import asyncio

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Telegram Bot Token
TELEGRAM_API_TOKEN = "7598394273:AAEv-PShPLKbYj8BoPKCD9Z3xQWYNPomMgc"

# Registered chat IDs
registered_users = {1981206622, 5311708356, 5863505513}
application = None


def login_to_twitter(driver):
    driver.get("https://x.com/login")
    time.sleep(3)

    username_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.NAME, 'text'))
    )
    username_input.send_keys("your-email@example.com")

    next_button = WebDriverWait(driver, 15).until(
        EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Next']"))
    )
    next_button.click()

    try:
        unusual_activity_input = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, "text"))
        )
        unusual_activity_input.send_keys("your-username")
        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/ancestor::button"))
        )
        next_button.click()
    except TimeoutException:
        pass

    password_input = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys("your-password")

    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
    )
    login_button.click()

    WebDriverWait(driver, 20).until(EC.url_changes("https://x.com/login"))
    print("Login successful")
    time.sleep(10)


async def send_alert_to_users(message: str):
    global application
    for chat_id in registered_users:
        try:
            await application.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")
        except Exception as e:
            print(f"Failed to send message to {chat_id}: {e}")


def scroll_and_collect_replies(driver, processed_urls, filtered_reply_links):
    scroll_count = 3
    for _ in range(scroll_count):
        current_time = datetime.now(timezone.utc)
        driver.execute_script("window.scrollBy(0, 650);")
        time.sleep(5)

        new_replies = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.XPATH, '//article[@data-testid="tweet"]'))
        )

        for reply in new_replies:
            try:
                url = reply.find_element(By.XPATH, './/time/parent::a').get_attribute('href')
                if url in processed_urls or url in filtered_reply_links:
                    continue

                time_text = reply.find_element(By.XPATH, './/time').get_attribute("datetime")
                post_time = datetime.fromisoformat(time_text.replace("Z", "+00:00"))
                minutes_since_posted = (current_time - post_time).total_seconds() / 60

                impressions_element = reply.find_element(By.XPATH,
                                                         ".//div[contains(@id, 'id__')]/div[4]/a/div/div[2]/span/span/span")
                impressions_text = impressions_element.text
                impressions_count = float(impressions_text.replace('K', '000').replace('M', '000000'))

                postImpression_ratio = impressions_count / minutes_since_posted if minutes_since_posted > 0 else 0
                if minutes_since_posted <= 300 and postImpression_ratio > 50:
                    filtered_reply_links.add(url)
                    alert_message = (
                        f"🚨 *New Reply Alert!*
                        f"🔗 [Click to view reply]({url})\n"
                        f"📊 *Impressions-to-Minutes Ratio:* {postImpression_ratio:.2f}\n"
                        f"⏱ *Minutes since posted:* {minutes_since_posted:.2f}"
                    )
                    asyncio.create_task(send_alert_to_users(alert_message))

                processed_urls.add(url)
            except StaleElementReferenceException:
                continue
    print(f"Collected {len(processed_urls)} unique replies.")


def run_scraper():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    login_to_twitter(driver)

    processed_urls = set()
    filtered_reply_links = set()
    last_reset_time = datetime.now()

    while True:
        if (datetime.now() - last_reset_time).total_seconds() >= 7200:
            processed_urls.clear()
            filtered_reply_links.clear()
            last_reset_time = datetime.now()

        driver.get("https://x.com/realonx1/with_replies")
        time.sleep(5)
        scroll_and_collect_replies(driver, processed_urls, filtered_reply_links)
        time.sleep(random.randint(20, 25) * 60)


def main():
    global application
    application = Application.builder().token(TELEGRAM_API_TOKEN).build()
    application.add_handler(CommandHandler("start", start))

    print("Starting Telegram bot and scraper...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_in_executor(None, run_scraper)
    application.run_polling()


if __name__ == "__main__":
    main()
