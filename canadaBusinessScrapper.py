import time
import pandas as pd
from seleniumbase import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
import re


def is_phone_number(text):
    # Define a regular expression pattern to match sequences of 8 or more digits
    pattern = r'\d'

    # Count the number of digit occurrences in the text
    digit_count = len(re.findall(pattern, text))

    # If there are 8 or more digits, consider it a phone number
    if digit_count >= 8:
        return True
    else:
        return False


start_time = time.time()
# Initialize the headless browser
driver = Driver(uc=True, headless=True)

url_file_path = "canada/2.british-columbia/surrey/url.txt"

current_row = 8

url_start_line = current_row  # Specify the line number where URLs start

with open(url_file_path, "r") as file:
    for line_number, url in enumerate(file, start=1):  # Start line numbering from 1
        if line_number >= url_start_line:
            url = url.strip()
            print(url)

            last_part = url.split("/")[-1]
            state = url.split("/")[4]

            driver.get(url)
            excel_file = 'canada/2.british-columbia/surrey/' + str(current_row) + '-' + state + '-' + last_part + '.xlsx'
            unique_urlfile_name = 'canada/2.british-columbia/surrey/' + str(
                current_row) + '-' + state + '-' + last_part + '.txt'

            try:
                total_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div/div[2]/div/h1/strong[1]'))
                )
                total = total_element.text
            except TimeoutException:
                total = 'Not Load'
            except Exception as e:
                total = 0

            print(total)
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
            empty = 'empty'
            each_row = 1

            data_xl = []

            # Open the file in write mode
            with open(unique_urlfile_name, 'w') as file:
                for unique_url in unique_urls_set:
                    file.write(str(unique_url) + '\n')

            total_unique_urls = len(unique_urls_set)
            print("Total unique URLs:", total_unique_urls)

            for unique_url in unique_urls_set:
                step_start_time = time.time()
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
                    try:
                        # Find the element with the first XPath
                        element1 = WebDriverWait(driver, 10).until(
                            EC.visibility_of_element_located(
                                (By.XPATH, '//*[@id="content"]/div[1]/div/header/div/div/h1/span[3]'))
                        )
                        business_name = element1.text
                        business_names.append(business_name)
                    except Exception as e:
                        business_name = empty
                        business_names.append(empty)

                id = 1
                try:
                    # Find the element with the second XPath
                    element2 = driver.find_element(By.XPATH,
                                                   '//*[@id="content"]/div[2]/div[2]/div[1]/div/div[1]/div/address')
                    address = element2.text
                    addresses.append(address)
                    id = 2
                except Exception as e:
                    date = 2
                    try:
                        # Find the element with the second XPath
                        element2 = driver.find_element(By.XPATH,
                                                       '//*[@id="content"]/div[2]/div[3]/div[1]/div/div[1]/div/address')
                        address = element2.text
                        addresses.append(address)
                        id = 3
                    except Exception as e:
                        try:
                            # Find the element with the second XPath
                            element2 = driver.find_element(By.XPATH,
                                                           '//*[@id="content"]/div[2]/div[4]/div[1]/div/div[1]/div/address')
                            address = element2.text
                            addresses.append(address)
                            id = 4
                        except Exception as e:
                            try:
                                # Find the element with the second XPath
                                element2 = driver.find_element(By.XPATH,
                                                               '//*[@id="content"]/div[2]/div[5]/div[1]/div/div[1]/div/address')
                                address = element2.text
                                addresses.append(address)
                                id = 5
                            except Exception as e:
                                print("Address Not Found")
                                addresses.append(empty)
                                address = empty

                try:
                    # Find the element with the third XPath
                    element3 = driver.find_element(By.XPATH,
                                                   '//*[@id="content"]/div[2]/div[' + str(id) + ']/div[1]/div/div[2]/a')
                    website = element3.get_attribute('href')
                    websites.append(website)
                except Exception as e:
                    websites.append(empty)
                    website = empty


                try:
                    phone_element = driver.find_element(By.CSS_SELECTOR, 'a[href^="tel:"]')
                    phone_number = phone_element.text
                    cleaned_phone_number = re.sub(r'\D', '', phone_number)
                    formatted_number = "1" + cleaned_phone_number
                    number = formatted_number
                    numbers.append(number)
                except Exception as e:
                    number = empty
                    numbers.append(empty)

                try:
                    element5 = driver.find_element(By.XPATH,
                                                   '//*[@id="content"]/div[3]/div/div[1]/div[1]/div/div[1]/dl/div[2]/dd')
                    business_open = element5.text
                    business_opens.append(business_open)
                except Exception as e:
                    try:
                        element5 = driver.find_element(By.XPATH,
                                                       '//*[@id="content"]/div[3]/div/div[1]/div[1]/div[2]/div[1]/dl/div[2]/dd')
                        business_open = element5.text
                        business_opens.append(business_open)
                    except Exception as e:
                        try:
                            element5 = driver.find_element(By.XPATH,
                                                           '//*[@id="content"]/div[3]/div/div[1]/div[1]/div[1]/div[1]/dl/div[3]/dd')
                            business_open = element5.text
                            business_opens.append(business_open)
                        except Exception as e:
                            business_open = empty
                            business_opens.append(empty)

                business_url.append(unique_url)
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

                data_xl.append({
                    'Business URL': unique_url,
                    'Business Name': business_name,
                    'Address': address,
                    'Website': website,
                    'Number': number,
                    'Business Open': business_open
                })
                df = pd.DataFrame(data_xl)
                df.to_excel(excel_file, index=False)

                print(
                    f"\n\nRow: {each_row} -> URL: {unique_url}, BN: {business_name}, Address: {address}, Website: {website}, Number: {number}, Business Open: {business_open}, STE: {step_time:.1f}s, TET: {execution_time}")
                each_row += 1

            print("Data saved to", excel_file)
            current_row += 1

driver.quit()
