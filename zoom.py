from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def login_to_zoom():
    email_address = 'bhargavigo.2022@gmail.com'  # Replace with your actual email address
    password = 'Bhargavi2346*'  # Replace with your actual password

    try:
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')
        chrome_options.add_argument('--disable-infobars')
        chrome_options.headless = False  # Set to True to run Chrome in headless mode

        # Use webdriver-manager to manage ChromeDriver
        service = Service(ChromeDriverManager().install())

        # Launch Chrome browser
        driver = webdriver.Chrome(service=service, options=chrome_options)

        # Navigate to the Zoom sign-in page
        driver.get('https://zoom.us/signin')

        try:
            # Fill out the email and password fields
            email_field = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, 'email')))
            email_field.send_keys(email_address)
            password_field = driver.find_element(By.NAME, 'password')
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            # Wait for the login process to complete
            WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#app > div > div > article > aside > div:nth-child(1) > div._meeting-widgets_cwepj_6 > a:nth-child(1) > span > div > img')))

            print("Logged in successfully")

            # Schedule a meeting
            schedule_meeting(driver)

        except Exception as login_exception:
            print("Error occurred while logging in:", login_exception)

        finally:
            # Close the browser
            driver.quit()

    except Exception as e:
        print("Error occurred:", e)

def schedule_meeting(driver):
    try:
        # Navigate to the meeting scheduling page
        driver.get('https://zoom.us/meeting/schedule')

        # Default wait time
        wait_time = 20  # Adjust this value to extend wait times

        # Wait for the meeting topic field to be present
        topic_field = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'topic')))
        topic_field.send_keys('Schedule Meeting')

        # Wait for the mt_time field to be present and interactable
        mt_time_field = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.ID, 'mt_time')))
        mt_time_field.click()  # Click to open the calendar
        mt_time_field.clear()  # Clear existing value
        mt_time_field.send_keys('06/04/2024')  # Send new date

        # Wait for the start_time field to be present
        start_time_field = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'start_time')))
        start_time_field.send_keys('09:20')

        # Wait for the am_pm field to be present
        am_pm_field = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'start_time2')))
        am_pm_field.send_keys('AM')

        # Wait for the agenda field to be present
        agenda_field = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'agenda')))
        agenda_field.send_keys('Test meeting agenda')

        # Wait for the duration select to be present
        duration_select = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'duration_time')))
        duration_select.send_keys('00:30')

        # Wait for the reminder checkbox to be present
        reminder_checkbox = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'dont_send_reminder')))
        reminder_checkbox.click()

        # Wait for the schedule button to be present
        schedule_button = WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.schedule-meeting')))
        schedule_button.click()

        # Wait for the meeting to be scheduled
        WebDriverWait(driver, wait_time).until(EC.presence_of_element_located((By.ID, 'schedule-meeting-success')))

        print("Meeting scheduled successfully")
    except Exception as e:
        print("Error occurred while scheduling the meeting:", e)

# Call the login_to_zoom function
login_to_zoom()
