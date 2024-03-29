import time
import pandas as pd
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup

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

            all_urls = []

            while True:
                try:
                    data_element = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[3]/div/div[1]/div[2]'))
                    )

                    html_content = data_element.get_attribute('outerHTML')
                    soup = BeautifulSoup(html_content, 'html.parser')
                    elements_with_class = soup.find_all(class_='text-blue-medium css-1jw2l11 eou9tt70')
                    urls = [element['href'] for element in elements_with_class if 'href' in element.attrs]

                    for url in urls:
                        all_urls.append(url)

                except TimeoutException:
                    print("Element not found.")
                    break
                except Exception as e:
                    print("Error while scraping data:", e)
                    break

                try:
                    next_button = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, 'a[rel="next"]'))  # Locate the "Next" link
                    )
                    driver.execute_script("arguments[0].scrollIntoView();", next_button)
                    next_button.click()
                    time.sleep(2)
                except TimeoutException:
                    print("Reached the last page.")
                    break
                except Exception as e:
                    print("Error while navigating to the next page:", e)
                    break

            unique_urls_set = set(all_urls)
            # Create empty lists to store extracted data
            business_url = []
            business_names = []
            addresses = []
            websites = []
            numbers = []
            business_opens = []
            empty = 'Empty'

            for unique_url in unique_urls_set:
                driver.get(unique_url)
                try:
                    # Find the element with the first XPath
                    element1 = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located(
                            (By.XPATH, '//*[@id="content"]/div[1]/div/header/div/div[2]/h1/span[3]'))
                    )
                    business_name = element1.text
                    business_names.append(business_name)
                except Exception as e:
                    print("Business Name Empty")
                    business_names.append(empty)

                try:
                    # Find the element with the second XPath
                    element2 = driver.find_element(By.XPATH,
                                                   '//*[@id="content"]/div[2]/div[2]/div[1]/div/div[1]/div/address')
                    address = element2.text
                    addresses.append(address)
                except Exception as e:
                    print("Address Not Found")
                    addresses.append(empty)

                try:
                    # Find the element with the third XPath
                    element3 = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[1]/div/div[2]/a')
                    website = element3.get_attribute('href')
                    websites.append(website)
                except Exception as e:
                    print("Website Not Found")
                    websites.append(empty)

                try:
                    # Find the element with the fourth XPath
                    element4 = driver.find_element(By.XPATH, '//*[@id="content"]/div[2]/div[2]/div[1]/div/div[3]/a')
                    number = element4.get_attribute('href')
                    numbers.append(number)
                except Exception as e:
                    print("Number Not Found")
                    numbers.append(empty)

                try:
                    # Find the element with the fifth XPath
                    element5 = driver.find_element(By.XPATH,
                                                   '//*[@id="content"]/div[3]/div/div[1]/div[1]/div/div[1]/dl/div[2]/dd')
                    business_open = element5.text
                    business_opens.append(business_open)
                except Exception as e:
                    print("Open Date Not Found")
                    business_opens.append(empty)

                business_url.append(unique_url)

                print(unique_url)

            # Create a dictionary from the lists
            data_dict = {
                'Business URL': business_url,
                'Business Name': business_names,
                'Address': addresses,
                'Website': websites,
                'Number': numbers,
                'Business Open': business_opens
            }

            # Create a DataFrame from the dictionary
            df = pd.DataFrame(data_dict)

            # Save the DataFrame to an Excel file
            excel_file = 'business/'+str(state)+'_'+str(line)+'.xlsx'
            df.to_excel(excel_file, index=False)

            print("Data saved to", excel_file)
            each_row+=1



driver.quit()
print("URLs saved to", output_excel_path)
