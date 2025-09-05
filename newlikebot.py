import asyncio
import os
import random
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from twikit import Client

# Initialize WebDriver
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

# Dictionary to track the latest replies
latest_replies = {}


async def login_twitter(client, account):
    """Login to Twitter using Twikit with cookies handling."""
    cookies_file = f'cookies_{account["auth_info_2"]}.json'

    if os.path.exists(cookies_file):
        client.load_cookies(cookies_file)
        if client.authenticated:
            print(f"✅ Logged in using saved cookies for {account['auth_info_2']}")
            return
        else:
            print(f"⚠️ Cookies expired for {account['auth_info_2']}, re-logging in...")

    await client.login(
        auth_info_1=account["auth_info_1"],
        auth_info_2=account["auth_info_2"],
        password=account["password"]
    )
    client.save_cookies(cookies_file)
    print(f"✅ Logged in and cookies saved for {account['auth_info_2']}")


async def like_reply(accounts, tweet_id):
    """Logs into accounts and likes a reply."""
    for account in accounts:
        client = Client()
        await login_twitter(client, account)

        try:
            await client.like(tweet_id)
            print(f"❤️ {account['auth_info_2']} liked reply {tweet_id}")
        except Exception as e:
            print(f"❌ Error liking tweet {tweet_id}: {e}")


def scrape_latest_replies(usernames, accounts):
    """Scrapes the latest replies and likes them immediately if new."""
    global latest_replies

    for username in usernames:
        profile_url = f"https://x.com/{username}/with_replies"
        driver.get(profile_url)
        time.sleep(random.uniform(3, 6))  # Random sleep to avoid detection

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, '//article[@data-testid="tweet"]'))
            )
            print(f"Page loaded for {username}, scraping replies...")
        except TimeoutException:
            print(f"Page took too long to load for {username}.")
            continue

        driver.execute_script("window.scrollBy(0, 700);")
        time.sleep(random.uniform(3, 6))

        tweets = driver.find_elements(By.XPATH, '//article[@data-testid="tweet"]')

        for i, tweet in enumerate(tweets[:4]):
            try:
                link = tweet.find_element(By.XPATH, './/time/parent::a')
                reply_url = link.get_attribute('href')
                tweet_id = reply_url.split("/")[-1]  # Extract tweet ID

                try:
                    replied_to_post = tweet.find_element(By.XPATH, './/a[contains(@href, "/status/")]')
                    replied_to_post_url = replied_to_post.get_attribute('href')
                except NoSuchElementException:
                    print("Could not find original post link.")
                    continue  # Skip if there's no original post

                timestamp = tweet.find_element(By.TAG_NAME, 'time').get_attribute('datetime')
                reply_time = datetime.fromisoformat(timestamp[:-1])

                if username in latest_replies and latest_replies[username]["reply"] == reply_url:
                    print(f"No new replies for {username}, skipping...")
                    continue  # No new reply

                latest_replies[username] = {"reply": reply_url, "original_post": replied_to_post_url}
                print(f"✅ New reply found for {username}: {reply_url}")

                # Immediately like the new reply
                asyncio.run(like_reply(accounts, tweet_id))

                break  # Stop checking after first new reply
            except NoSuchElementException:
                print(f"Reply {i + 1} not found for {username}.")
                continue


# Twitter accounts with credentials
twitter_accounts = [
    {"auth_info_1": "user1", "auth_info_2": "email1", "password": "pass1"},
    {"auth_info_1": "user2", "auth_info_2": "email2", "password": "pass2"},
    {"auth_info_1": "user3", "auth_info_2": "email3", "password": "pass3"},
    {"auth_info_1": "user4", "auth_info_2": "email4", "password": "pass4"},
]

# List of usernames to scrape replies from
usernames = ["UTDTrey", "transmarisa", "dribrazill", "YourQueenAmelia"]

# Run scraper
scrape_latest_replies(usernames, twitter_accounts)
