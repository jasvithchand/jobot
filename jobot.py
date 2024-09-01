import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
import time

# Function to handle actions specific to "My Information" step
def handle_how_did_you_hear(driver):
    """Handle the 'How Did You Hear About Us?' field by directly entering 'LinkedIn Jobs' and pressing Enter."""
    try:
        # Wait for the field to be clickable
        hear_about_us_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="input-1"]'))
        )

        # Clear the field (in case there's any default value)
        hear_about_us_field.clear()

        # Directly enter "LinkedIn Jobs"
        hear_about_us_field.send_keys("LinkedIn Jobs")
        print("Entered 'LinkedIn Jobs' into 'How Did You Hear About Us?' field")

        # Press Enter to lock in the value
        hear_about_us_field.send_keys(Keys.RETURN)
        print("Pressed Enter to lock in the value")

        # Click elsewhere on the page to lose focus
        body = driver.find_element(By.TAG_NAME, 'body')
        body.click()
        print("Clicked elsewhere to lose focus")

        time.sleep(1)

    except TimeoutException as e:
        print(f"Timeout occurred while handling 'How Did You Hear About Us?' field: {e}")
    except Exception as e:
        print(f"An error occurred while handling 'How Did You Hear About Us?' field: {e}")


def handle_my_information_step(driver):
    """Handle form filling in the 'My Information' step."""
    try:
        # Handle 'How Did You Hear About Us?' field
        handle_how_did_you_hear(driver)

        # previously_worked_no = WebDriverWait(driver, 10).until(
        #     EC.element_to_be_clickable((By.XPATH, '//*[@id="2"]'))
        # )
        # previously_worked_no.click()
        # print("Clicked 'Previously worked' No option")

        time.sleep(1)

        # Click the country dropdown to open it
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="input-3"]'))
        )
        dropdown.click()
        print("Clicked country dropdown")

        # Wait for the dropdown options to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//li[@role='option']//div[contains(text(), 'United States of America')]"))
        )

        # Find and click the "United States of America" option
        usa_option = driver.find_element(By.XPATH, "//li[@role='option']//div[contains(text(), 'United States of America')]")
        driver.execute_script("arguments[0].scrollIntoView();", usa_option)
        ActionChains(driver).move_to_element(usa_option).click().perform()
        print("Selected 'United States of America' from dropdown")

        # # Wait for the selection to be reflected in the input
        # WebDriverWait(driver, 10).until(
        #     EC.text_to_be_present_in_element_value((By.XPATH, '//*[@id="input-3"]'), "United States of America")
        # )
        # print("Confirmed 'United States of America' is selected")

        # # Wait for the selection to be reflected in the input
        # WebDriverWait(driver, 10).until(
        #     EC.text_to_be_present_in_element_value((By.XPATH, '//*[@id="input-3"]'), "United States of America")
        # )
        # print("Confirmed 'United States of America' is selected")

        # Handle FirstName
        first_name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['inputFirstName']))
        )
        first_name_field.clear()
        first_name_field.send_keys(user_data['FirstName'])
        print("Entered FirstName")

        # Handle LastName
        last_name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['inputLastName']))
        )
        last_name_field.clear()
        last_name_field.send_keys(user_data['LastName'])
        print("Entered LastName")

        # Handle Address Line 1
        address_line_1_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['inputAddress1']))
        )
        address_line_1_field.clear()
        address_line_1_field.send_keys(user_data['AddressLine1'])
        print("Entered Address Line 1")

        # Handle City
        city_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['inputCity']))
        )
        city_field.clear()
        city_field.send_keys(user_data['City'])
        print("Entered City")

        #Handle State
        # Open the state dropdown
        state_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['stateDropdown']))
        )
        state_dropdown.click()
        print("State dropdown clicked")

        # Wait for the state option to be visible
        state_to_select = user_data['State']  # Make sure 'State' is correctly named in userinfo.json
        state_option_xpath = xpaths['stateOption'].replace('{state}', state_to_select)
        state_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, state_option_xpath))
        )

        # Click the state option
        driver.execute_script("arguments[0].scrollIntoView();", state_option)
        state_option.click()
        print(f"Selected state: {state_to_select}")
        time.sleep(1)

        # Handle Postal Code
        postal_code_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['inputPostalcode']))
        )
        postal_code_field.clear()
        postal_code_field.send_keys(user_data['PostalCode'])
        print("Entered Postal Code")

        # Click the device type dropdown to open it
        device_dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['deviceTypeDropdown']))
        )
        device_dropdown.click()
        print("Device type dropdown clicked")

        # Wait for the device type option to be visible
        device_type = user_data['PhoneDeviceType']  # Ensure this key exists in userinfo.json
        device_option_xpath = xpaths['deviceTypeOption'].replace('{device_type}', device_type)
        device_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, device_option_xpath))
        )

        # Click the device type option
        driver.execute_script("arguments[0].scrollIntoView();", device_option)
        device_option.click()
        print(f"Selected device type: {device_type}")
        time.sleep(1)

        # Handle Phone Number
        phone_number_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['inputPhoneNumber']))
        )
        phone_number_field.clear()
        phone_number_field.send_keys(user_data['PhoneNumber'])
        print("Entered Phone Number Code")

        # Click on "Save and Continue"
        save_and_continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['myInformationSubmit']))
        )
        save_and_continue_button.click()
        print("Clicked 'Save and Continue' button.")

        # Ensure navigation to the next step
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[contains(text(), "My Experience")]'))
        )
        print("Navigated to 'My Experience' step.")




    except TimeoutException as e:
        print(f"Timeout occurred while handling 'My Information' step: {e}")
    except NoSuchElementException as e:
        print(f"Element not found while handling 'My Information' step: {e}")
    except ElementClickInterceptedException as e:
        print(f"Element click was intercepted: {e}")
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
    time.sleep(1)

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
    time.sleep(40)
    driver.quit()
