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
import os

def handle_voluntary_disclosures(driver):

    #Handle Gender
    # Open the gender dropdown
    gender_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpaths['genderDropdown']))
    )
    gender_dropdown.click()
    print("Gender dropdown clicked")

    time.sleep(1)

    # Wait for the gender option to be visible
    gender_to_select = user_data['gender']  # Make sure 'State' is correctly named in userinfo.json
    gender_option_xpath = xpaths['genderOption'].replace('{gender}', gender_to_select)
    gender_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, gender_option_xpath))
    )

    time.sleep(1)

    # Click the gender option
    driver.execute_script("arguments[0].scrollIntoView();", gender_option)
    gender_option.click()
    print(f"Selected gender: {gender_to_select}")
    time.sleep(1)


    # Check "I agree to the terms and conditions"
    try:
        # Wait for any known obstructions to disappear
        driver.switch_to.active_element
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['agreementCheckbox']))
        )
        driver.find_element(By.XPATH, xpaths['agreementCheckbox']).click()
        print("Clicked 'I agree to the terms and conditions' checkbox.")
    except (NoSuchElementException, TimeoutException):
        print("Agreement checkbox not found.")
        pass

    time.sleep(1)




#Function to handle My experience Page
def handle_my_experience_step(driver):
    """Handles interactions in the 'My Experience' section."""

    try:
        # Click on "Add" in Work Experience
        add_experience_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['addExperienceButton']))
        )
        add_experience_button.click()
        print("Clicked 'Add' button.")
    except Exception as e:
        print(f"An error occurred while clicking 'Add' button: {e}")

    time.sleep(5)

    #Click Add Another Work Experience
    try:
        button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-label='Add Another Work Experience']"))
        )
        driver.execute_script("arguments[0].click();", button)
        print("Clicked 'Add Another' button in Experience.")

    except (NoSuchElementException,TimeoutException):
        print("Add Another Work Experience button not found")
        pass

    time.sleep(1)


    def enter_work_experience_details(driver):
        try:
            # Fetch all inputs for job titles, company, location, and role descriptions based on their data-automation-id
            job_titles = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[data-automation-id='jobTitle']"))
            )
            companies = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[data-automation-id='company']"))
            )
            locations = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[data-automation-id='location']"))
            )
            role_descriptions = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "textarea[data-automation-id='description']"))
            )
            from_months = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[data-automation-id='dateSectionMonth-input']"))
            )
            from_years = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[data-automation-id='dateSectionYear-input']"))
            )

            # Iterate over each set of fields found
            for index, (job_title_input, company_input, location_input, role_description_input) in enumerate(
                zip(job_titles, companies, locations, role_descriptions), start=1):

                # Job Title
                job_title_key = f"JobTitle{index:02}"
                if job_title_key in user_data:
                    job_title_input.clear()
                    job_title_input.send_keys(user_data[job_title_key])
                    print(f"Entered {user_data[job_title_key]} for Job Title {index}.")

                # Company
                company_key = f"Company{index:02}"
                if company_key in user_data:
                    company_input.clear()
                    company_input.send_keys(user_data[company_key])
                    print(f"Entered {user_data[company_key]} for Company {index}.")

                # Location
                location_key = f"Location{index:02}"
                if location_key in user_data:
                    location_input.clear()
                    location_input.send_keys(user_data[location_key])
                    print(f"Entered {user_data[location_key]} for Location {index}.")

                # Role Description
                description_key = f"RoleDescription{index:02}"
                if description_key in user_data:
                    role_description_input.clear()
                    role_description_input.send_keys(user_data[description_key])
                    print(f"Entered {user_data[description_key]} for Role Description {index}.")
            
            for i in range(0, len(from_months)-1):
                index = i // 2 + 1  # Determine which work experience entry we are dealing with based on the index
                month_key = f"FromMonth{index:02}"
                year_key = f"FromYear{index:02}"

                # Enter "From" dates
                if month_key in user_data and year_key in user_data:
                    from_months[i].clear()
                    from_months[i].send_keys(user_data[month_key])
                    from_years[i].clear()
                    from_years[i].send_keys(user_data[year_key])
                    print(f"Entered 'From' dates for experience {index}: {user_data[month_key]}/{user_data[year_key]}")

                # Check if 'To' dates need to be entered
                to_month_key = f"toMonth{index:02}"
                to_year_key = f"toYear{index:02}"
                # Ensure there is a corresponding 'To' month/year field and user data provides the 'To' info
                if to_month_key in user_data and to_year_key in user_data and (i+1 < len(from_months)):
                    from_months[i+1].clear()
                    from_months[i+1].send_keys(user_data[to_month_key])
                    from_years[i+1].clear()
                    from_years[i+1].send_keys(user_data[to_year_key])
                    print(f"Entered 'To' dates for experience {index}: {user_data[to_month_key]}/{user_data[to_year_key]}")

        except Exception as e:
            print(f"An error occurred while entering work experience details: {e}")

    enter_work_experience_details(driver)

    # Click elsewhere on the page to lose focus
    body = driver.find_element(By.TAG_NAME, 'body')
    body.click()
    print("Clicked elsewhere to lose focus")

    driver.switch_to.default_content()

    # Check "I currently work here"
    try:
        # Wait for any known obstructions to disappear
        driver.switch_to.active_element
        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['currentWorkCheckbox']))
        )
        driver.find_element(By.XPATH, xpaths['currentWorkCheckbox']).click()
        print("Clicked 'I currently work here' checkbox.")
    except (NoSuchElementException, TimeoutException):
        print("Current work checkbox not found.")
        pass

    #Enter School Name
    try:
        school_name_field = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['inputEducationSchoolName']))
        )
        school_name_field.clear()
        school_name_field.send_keys(user_data['school_name'])
        print("Entered School Name.")
    except Exception as e:
        print(f"An error occurred while entering school name: {e}")

    #Handle Degree
    # Open the degree dropdown
    degree_dropdown = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, xpaths['degreeDropdown']))
    )
    degree_dropdown.click()
    print("Degree dropdown clicked")

    time.sleep(1)

    # Wait for the degree option to be visible
    degree_to_select = user_data['degree']  # Make sure 'degree' is correctly named in userinfo.json
    degree_option_xpath = xpaths['degreeOption'].replace('{degree}', degree_to_select)
    degree_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, degree_option_xpath))
    )

    time.sleep(1)

    # Click the degree option
    driver.execute_script("arguments[0].scrollIntoView();", degree_option)
    degree_option.click()
    print(f"Selected degree: {degree_to_select}")
    time.sleep(1)


    # #Add Education
    # try:
    #     add_education_button = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, xpaths['addEducationButton']))
    #     )
    #     add_education_button.click()
    #     print("Clicked 'Add Education' button.")
    # except Exception as e:
    #     print(f"An error occurred while adding education: {e}")

    # #Enter Skills
    # try:
    #     skills_field = WebDriverWait(driver, 10).until(
    #         EC.element_to_be_clickable((By.XPATH, xpaths['inputSkills']))
    #     )
    #     skills_field.clear()
    #     skills_field.send_keys(user_data['skills'])
    #     print("Entered Skills.")
    # except Exception as e:
    #     print(f"An error occurred while entering skills: {e}")
    #     pass
    
    #upload resume
    delete_resumes = driver.find_elements(By.CSS_SELECTOR, "button[data-automation-id='delete-file']")
    i = 1
    while i <= len(delete_resumes):
      driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='delete-file']").click()
      i = i+1
      time.sleep(1)
    clear
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.clear()
    file_input.send_keys(os.path.abspath(user_data['resume_path']))
    time.sleep(5)

    #Add Websites
    try:
        add_websites_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, xpaths['addWebsitesButton']))
        )
        add_websites_button.click()
        print("Clicked 'Add Websites' button.")
        time.sleep(0.5)
        input_website_url = driver.find_element(By.XPATH, xpaths['inputWebsiteUrl'])
        input_website_url.clear()
        input_website_url.send_keys(user_data['website_url'])
        print("Entered Website URL.")

        time.sleep(1)

    except Exception as e:
        print(f"An error occurred while adding websites: {e}")
    
    #Add LinkedIn
    try:
      linkedin_question = driver.find_element(By.CSS_SELECTOR, "input[type='text'][data-automation-id='linkedinQuestion']")
      linkedin_question.clear()
      linkedin_question.send_keys(user_data['linkedin_url'])
      print("Entered LinkedIn URL.")
    except:
      print("Exception: 'No Linkedin input'")


def click_next(driver):
    try:
        # Click the 'Next' button
        button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-automation-id='bottom-navigation-next-button']")))
        button.click()

        # Check for errors after clicking the button
        try:
            error_button = driver.find_element(By.CSS_SELECTOR, "button[data-automation-id='errorBanner']")
            print("Exception: 'Errors on page. Please resolve and submit manually. You have 60 seconds to do so!'")
            time.sleep(60)  # Wait to manually resolve errors
        except NoSuchElementException:
            print("No Errors")

        # Wait to ensure any post-click actions complete
        time.sleep(3)
    except Exception as e:
        print(f"An error occurred while clicking 'Next' button: {e}")   

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

        try:
            driver.switch_to.active_element
            driver.find_element(By.CSS_SELECTOR, "input[type='radio'][data-uxi-element-id='radio_2']").click()
            print("Clicked 'Previously worked' No option - 2")
        except:
            print("Exception: 'No radio_2 button'")

        time.sleep(1)

        # Click the country dropdown to open it
        dropdown = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="input-3"]'))
        )
        dropdown.click()
        print("Clicked country dropdown")

        time.sleep(0.5)

        # Wait for the dropdown options to be visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//li[@role='option']//div[contains(text(), 'United States of America')]"))
        )

        # Find and click the "United States of America" option
        usa_option = driver.find_element(By.XPATH, "//li[@role='option']//div[contains(text(), 'United States of America')]")
        driver.execute_script("arguments[0].scrollIntoView();", usa_option)
        ActionChains(driver).move_to_element(usa_option).click().perform()
        print("Selected 'United States of America' from dropdown")

        # Handle FirstName
        try:
            first_name_field = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, xpaths['inputFirstName']))
            )
            first_name_field.clear()
            first_name_field.send_keys(user_data['FirstName'])
            print("Entered FirstName")
        except Exception as e:
            print(f"An error occurred filling first name: {e}")



        # Handle LastName
        try:
            driver.find_element(By.CSS_SELECTOR, "input[type='text'][data-automation-id='legalNameSection_lastName']").clear()
            time.sleep(1)
            driver.find_element(By.CSS_SELECTOR, "input[type='text'][data-automation-id='legalNameSection_lastName']").send_keys(user_data['LastName'])
            print("Entered LastName")
        except Exception as e:
            print(f"An error occurred filling last name: {e}")


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

        time.sleep(1)

        # Wait for the state option to be visible
        state_to_select = user_data['State']  # Make sure 'State' is correctly named in userinfo.json
        state_option_xpath = xpaths['stateOption'].replace('{state}', state_to_select)
        state_option = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, state_option_xpath))
        )

        time.sleep(1)

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

        time.sleep(1)

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
        driver.execute_script("arguments[0].scrollIntoView();", save_and_continue_button)
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

actions = ActionChains(driver)

# Navigate to the login page using the URL from the URLs file
driver.get(urls['loginUrl'])

try:
    # Use Email and Password from user info
    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, xpaths['emailInput'])))
    email_input.send_keys(user_data['email'])
    password_input = driver.find_element(By.XPATH, xpaths['passwordInput'])
    password_input.send_keys(user_data['password'])
    time.sleep(0.5)

    # Click the Sign-In Button
    sign_in_button = driver.find_element(By.XPATH, xpaths['signInButton'])
    ActionChains(driver).move_to_element(sign_in_button).click().perform()
    time.sleep(0.5)

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
        click_next(driver)
        current_step = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[3]/h2')
        current_step = current_step_header.text
        print(f"Currently at: {current_step}")
        handle_my_experience_step(driver)
        click_next(driver)
        current_step = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[3]/h2')
        current_step = current_step_header.text
        print(f"Currently at: {current_step}")
        handle_voluntary_disclosures(driver)
        click_next(driver)
        current_step = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[3]/h2')
        current_step = current_step_header.text
        print(f"Currently at: {current_step}")

        #Final Submit
        click_next(driver)
        time.sleep(10)

        #driver.quit()

    else:
        print(f"Unexpected step: {current_step}")

    # Update current application step
    current_step_header = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div/div[3]/h2')
    current_step = current_step_header.text
    print(current_step)

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
