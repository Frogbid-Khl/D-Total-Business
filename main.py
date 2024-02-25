import time
import pandas as pd
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

start_time = time.time()
# Initialize the headless browser
driver = Driver(uc=True, headless=True)

site_url = "https://www.bbb.org/"

category_file_path = "input/category.txt"  # Update the file path with your file

country_file_path = "input/country.xlsx"  # Update the file path with your Excel file

output_excel_path = "output/business.xlsx"

columns_to_read = ["Country", "State", "Business", "State Name"]

# Read the specified columns from the Excel file
data = pd.read_excel(country_file_path, usecols=columns_to_read)

data_xl = []
each_row=1
# Iterate over each row
for index, row in data.iterrows():
    # Process each row here
    country = row["Country"]
    state = row["State"]
    business = row["Business"]
    state_full_name = row["State Name"]
    with open(category_file_path, "r") as file:
        for line in file:
            step_start_time = time.time()
            line = line.strip().lower()  # Convert to lowercase and remove trailing newline characters
            line = line.replace(' ', '-')  # Replace spaces with hyphens
            url = site_url + country + "/" + business + "/category/" + line

            driver.get(url)

            try:
                # Explicitly wait for the element to be visible
                total_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/div/h1/strong[1]'))
                )
                total = total_element.text
            except TimeoutException:
                total = 'Not Load'
            except Exception as e:
                total = 0

            step_time = time.time() - step_start_time
            total_time = time.time() - start_time

            # Convert seconds to days, hours, minutes, and seconds
            total_days, remainder = divmod(total_time,
                                           86400)  # 60 seconds * 60 minutes * 24 hours = 86400 seconds
            total_hours, remainder = divmod(remainder, 3600)  # 60 minutes * 60 seconds = 3600 seconds
            total_minutes, total_seconds = divmod(remainder, 60)

            # Construct the concise form of the execution time
            execution_time = ""
            if total_days >= 1:
                execution_time += f"{int(total_days)}d "
            if total_hours >= 1:
                execution_time += f"{int(total_hours)}h "
            if total_minutes >= 1:
                execution_time += f"{int(total_minutes)}m "

            execution_time += f"{int(total_seconds)}s"

            data_xl.append({'State': state_full_name, 'URL': url, 'Total': total})
            print(f"Row: {each_row} -> State: {state_full_name}, URL: {url}, Total: {total}, STE: {step_time:.1f}s, TET: {execution_time}")

            df = pd.DataFrame(data_xl)
            df.to_excel(output_excel_path, index=False)
            each_row+=1




driver.quit()
print("URLs saved to", output_excel_path)
