from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from getpass import getpass
import requests
from datetime import datetime

# Config
ESR_URL = "https://my.esr.nhs.uk/dashboard/web/"
GOV_HOLIDAYS_URL = "https://www.gov.uk/bank-holidays.json"

ESR_USERNAME = ''
print(f"Username: {ESR_USERNAME}")
ESR_PASSWORD = getpass('Password:')

TEST_MODE = 1 # test mode when set won't actually attempt to add entries

# Fetch and filter bank holidays
print(f"Copying bank holidays from {GOV_HOLIDAYS_URL}")

with requests.get(GOV_HOLIDAYS_URL) as response:
    if response.status_code != 200:
        print(f"Error fetching holidays: {response.status_code}")
        exit(1)

    data = response.json()
    current_year = datetime.now().year
    next_year = current_year + 1

    #filter json dictionary for holidays that fall in the current financial year, which runs from April 1st of the current year to March 31st of the next year, and sort them by date.
    filtered_holidays = sorted(
        [h for h in data['england-and-wales']['events']
         if (h_date := datetime.strptime(h['date'], "%Y-%m-%d")).year in {current_year, next_year} and
         (h_date.year == current_year and h_date.month >= 4 or h_date.year == next_year and h_date.month < 4)],
        key=lambda x: x['date']
    )

print(f"Logging into ESR at {ESR_URL}")

# Initialise Selenium WebDriver
driver = webdriver.Chrome()
driver.get(ESR_URL)

# Login
driver.find_element(By.NAME, "username").send_keys(ESR_USERNAME)
driver.find_element(By.NAME, "password").send_keys(ESR_PASSWORD + Keys.RETURN)
wait = WebDriverWait(driver, 10)

# Find the <select> element of assignment
select_element = driver.find_element("id", "select-an-assignment")

# Wrap it with Select class
select = Select(select_element)

# Get the current id from the assignment drop down
item_id = select.first_selected_option.get_attribute("value")

# Process bank holidays
print(f"Processing bank holidays")
for holiday in filtered_holidays:
    formatted_date = datetime.strptime(holiday['date'], "%Y-%m-%d").strftime("%d/%m/%Y") 
    print(f"Adding Bank Holiday: {holiday['date']} - {holiday['title']}")

    wait.until(EC.visibility_of_element_located((By.XPATH, "//a[@id='createAnnualLeave']"))).click()

    Select(driver.find_element(By.ID, "select-leave-reason-" + item_id)).select_by_visible_text("Bank Holiday")

    # Clear and send the "absenceComments" field
    absenceCommentsInput = driver.find_element(By.NAME, "absenceComments")
    absenceCommentsInput.clear()
    absenceCommentsInput.send_keys(holiday["title"] + "\nAdded via MRB Bank Holiday Python Script")

    # Clear and send the "startDateInput" field
    startDateInput = driver.find_element(By.ID, "startDateInput")
    startDateInput.clear()
    startDateInput.send_keys(formatted_date)

    # Clear and send the "startDateInput" field
    endDateInput = driver.find_element(By.ID, "endDateInput")
    endDateInput.clear()
    endDateInput.send_keys(formatted_date)

    if (TEST_MODE == 1):
        finalInput = driver.find_element(By.XPATH, "//a[text()='Cancel']")
    else:
        finalInput = driver.find_element(By.XPATH, "//a[@id='submitAnnualLeave']")
        wait.until(EC.invisibility_of_element_located((By.ID, "requestProcessedModalId")))

    finalInput.click()
      
    print("Bank holiday added, continuing...")

print("All bank holidays added. Closing browser.")
driver.quit()
