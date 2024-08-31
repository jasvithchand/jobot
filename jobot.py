import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

# Function to handle actions specific to "My Information" step
def handle_my_information_step(driver):
    """Handle form filling in the 'My Information' step."""
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@id="input-1"]'))
        )
        source_input = driver.find_element(By.XPATH, '//*[@id="input-1"]')
        source_input.send_keys("Linkedin Jobs")
        print("Filled 'Source' input")

        previously_worked_no = driver.find_element(By.XPATH, '//*[@id="2"]')
        previously_worked_no.click()
        print("Clicked 'Previously worked' No option")

        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="input-3"]'))
        )
        dropdown.click()
        print("Clicked country dropdown")

        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@role='option' and contains(text(), 'United States of America')]"))
        )
        option.click()
        print("Selected 'United States of America' from dropdown")

    except TimeoutException as e:
        print(f"Timeout occurred while handling 'My Information' step: {e}")
    except NoSuchElementException as e:
        print(f"Element not found while handling 'My Information' step: {e}")
    except Exception as e:
        print(f"An error occurred while handling 'My Information' step: {e}")

# Function to handle the account creation process
def handle_failed_login(driver):
    """Handle account creation if login fails."""
    try:
        create_account_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, xpaths['createAccountButton']))
        )
        ActionChains(driver).move_to_element(create_account_button).click().perform()

        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, xpaths['newAccountEmail'])))
        driver.find_element(By.XPATH, xpaths['newAccountEmail']).send_keys(user_data['email'])
        driver.find_element(By.XPATH, xpaths['newAccountPassword']).send_keys(user_data['password'])
        driver.find_element(By.XPATH, xpaths['newAccountConfirmPassword']).send_keys(user_data['password'])

        agree_checkbox = driver.find_element(By.XPATH, xpaths['agreeCheckbox'])
        agree_checkbox.click()

        create_account_submit_button = driver.find_element(By.XPATH, xpaths['submitCreateAccount'])
        ActionChains(driver).move_to_element(create_account_submit_button).click().perform()

        print("Account creation attempted.")
    except Exception as e:
        print(f"An error occurred during account creation: {e}")

# Load user info, xpaths, and urls from JSON files
with open('userinfo.json', 'r') as file:
    user_data = json.load(file)
with open('xpaths.json', 'r') as file:
    xpaths = json.load(file)
with open('urls.json', 'r') as file:
    urls = json.load(file)

# Path to your EdgeDriver
driver_path = 'driver/edgedriver_mac64_m1/msedgedriver'
service = Service(executable_path=driver_path)

# Initialize the WebDriver
driver = webdriver.Edge(service=service)

# Navigate to the login page using the URL from the URLs file
driver.get(urls['loginUrl'])

try:
    # Use Email and Password from user info
    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['emailInput'])))
    email_input.send_keys(user_data['email'])
    password_input = driver.find_element(By.XPATH, xpaths['passwordInput'])
    password_input.send_keys(user_data['password'])

    # Click the Sign-In Button
    sign_in_button = driver.find_element(By.XPATH, xpaths['signInButton'])
    ActionChains(driver).move_to_element(sign_in_button).click().perform()

    # Wait for the page to load after login
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="mainContent"]/div/div[3]/h2'))
    )
    print("Login successful, redirected to another page.")

    # Detect the current application step
    current_step_header = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[3]/h2')
    current_step = current_step_header.text
    print(f"Currently at: {current_step}")

    if "My Information" in current_step:
        handle_my_information_step(driver)
    else:
        print(f"Unexpected step: {current_step}")

except TimeoutException as e:
    print(f"Timeout occurred: {e}")
    print("Current URL:", driver.current_url)
    print("Page source:", driver.page_source[:500])  # Print first 500 characters of page source
    handle_failed_login(driver)

except Exception as e:
    print(f"An error occurred: {e}")
    print("Current URL:", driver.current_url)
    print("Page source:", driver.page_source[:500])  # Print first 500 characters of page source

finally:
    # Optionally keep the browser open for debugging
    time.sleep(20)
    driver.quit()
