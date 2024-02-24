from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize the headless browser
driver = Driver(uc=True, headless=True)

# Navigate to the URL
driver.get("https://www.bbb.org/us/wy/cheyenne/category/wood-rot-repair")

try:
    # Explicitly wait for the element to be visible
    total_element = WebDriverWait(driver, 30).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/div/h1/strong[1]'))
    )
    total = total_element.text
    print(total)
except TimeoutException:
    print("Timed out waiting for total element to load")
except Exception as e:
    print("Error:", e)

# Quit the browser
driver.quit()
