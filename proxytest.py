import zipfile
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

# Account and proxy details
accounts = [
    {
        'email': 'latestjoboffers7@gmail.com',
        'username': 'Babymartxxx',
        'password': 'Krish@6969',
        'proxy': {'host': '130.255.65.186', 'port': '12323', 'user': '14acc5b4cccca', 'pass': '8b9286578b'}
    },
    {
        'email': 'evamillerxo',
        'username': 'evamillerxo',
        'password': 'krish@6969',
        'proxy': {'host': 'proxy2_host', 'port': 'proxy2_port', 'user': 'proxy2_user', 'pass': 'proxy2_pass'}
    },
    # Add more accounts as needed...
]

# Path to ChromeDriver
chrome_driver_path = r"C:\selenium\chromedriver-win64\chromedriver.exe"
service = Service(chrome_driver_path)

# Function to create a proxy extension
def create_proxy_extension(proxy):
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Proxy Auth Extension",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        }
    }
    """

    background_js = f"""
    var config = {{
        mode: "fixed_servers",
        rules: {{
            singleProxy: {{
                scheme: "http",
                host: "{proxy['host']}",
                port: parseInt({proxy['port']})
            }},
            bypassList: ["localhost"]
        }}
    }};

    chrome.proxy.settings.set({{value: config, scope: "regular"}}, function() {{}});

    chrome.webRequest.onAuthRequired.addListener(
        function(details) {{
            return {{
                authCredentials: {{
                    username: "{proxy['user']}",
                    password: "{proxy['pass']}"
                }}
            }};
        }},
        {{urls: ["<all_urls>"]}},
        ["blocking"]
    );
    """

    # Save the extension files
    with zipfile.ZipFile("proxy_auth_extension.zip", "w") as zipf:
        zipf.writestr("manifest.json", manifest_json)
        zipf.writestr("background.js", background_js)

# Function to log in and like replies
def login_and_like(account):
    # Create proxy extension
    create_proxy_extension(account['proxy'])
    chrome_options = Options()
    chrome_options.add_extension("proxy_auth_extension.zip")

    # Initialize WebDriver
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        # Open Twitter login page
        driver.get("https://twitter.com/login")
        time.sleep(random.uniform(2, 4))

        # Log in to the account
        username_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.NAME, 'text'))
        )
        username_input.send_keys(account['email'])

        # Click 'Next' button
        next_button = WebDriverWait(driver, 15).until(
            EC.element_to_be_clickable((By.XPATH, "//button//span[text()='Next']"))
        )
        next_button.click()

        try:
            # Handle unusual activity input if present
            unusual_activity_input = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.NAME, "text"))
            )
            unusual_activity_input.send_keys(account['username'])
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']/ancestor::button"))
            )
            next_button.click()
        except TimeoutException:
            print("No unusual activity page detected.")

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
        print(f"Logged in successfully for {account['username']}")

        # Navigate to the reply and like it
        driver.get("https://x.com/evamillerxo/with_replies")  # Replace with the actual reply URL
        time.sleep(random.uniform(4, 6))
        
        driver.execute_script(f"window.scrollBy(0, {550});")
        
        like_buttons = driver.find_elements(By.XPATH, "//div[starts-with(@id, 'id__')]/div[3]/button/div/div[1]/div")
        print(f"Found {len(like_buttons)} potential like buttons.")

        # Like the first two buttons only
        for like_button in like_buttons[:2]:
            try:
                color = like_button.value_of_css_property("color")
                if color == "rgba(249, 24, 128, 1)":
                    print("Already liked")
                else:
                    print("Liking")
                    driver.execute_script("arguments[0].scrollIntoView(true);", like_button)
                    time.sleep(0.5)
                    driver.execute_script("arguments[0].click();", like_button)
                    time.sleep(2)
            except (ElementClickInterceptedException, NoSuchElementException):
                print("Error interacting with like button.")

    except TimeoutException:
        print("Login failed or an element could not be located in time.")
    finally:
        driver.quit()

# Loop through accounts
for account in accounts:
    login_and_like(account)
    time.sleep(random.uniform(30, 60))  # Delay between accounts
