import pandas as pd
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Initialize the headless browser
driver = Driver(uc=True, headless=True)

site_url = "https://www.bbb.org/"

category_file_path = "input/category.txt"  # Update the file path with your file

country_file_path = "input/country.xlsx"  # Update the file path with your Excel file

columns_to_read = ["Country", "State", "Business", "State Name"]

# Read the specified columns from the Excel file
data = pd.read_excel(country_file_path, usecols=columns_to_read)

data_xl = []

# Iterate over each row
for index, row in data.iterrows():
    # Process each row here
    country = row["Country"]
    state = row["State"]
    business = row["Business"]
    state_full_name = row["State Name"]
    with open(category_file_path, "r") as file:
        for line in file:
            line = line.strip().lower()  # Convert to lowercase and remove trailing newline characters
            line = line.replace(' ', '-')  # Replace spaces with hyphens
            url = site_url + country + "/" + business + "/category/" + line

            driver.get(url)

            try:
                # Explicitly wait for the element to be visible
                total_element = WebDriverWait(driver, 30).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/div/h1/strong[1]'))
                )
                total = total_element.text
            except TimeoutException:
                total = 'Not Load'
            except Exception as e:
                total = 0

            data_xl.append({'State': state_full_name, 'URL': url, 'Total': total})
            print(f"State: {state_full_name}, URL: {url}, Total: {total}")

            df = pd.DataFrame(data_xl)

            output_excel_path = "output/business.xlsx"
            df.to_excel(output_excel_path, index=False)

driver.quit()
print("URLs saved to", output_excel_path)
