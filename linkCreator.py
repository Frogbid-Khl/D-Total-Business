import pandas as pd

site_url = "https://www.bbb.org/"

category_file_path = "input/category.txt"  # Update the file path with your file

country_file_path = "input/country.xlsx"  # Update the file path with your Excel file

columns_to_read = ["Country", "State", "Business", "State Name"]

# Read the specified columns from the Excel file
data = pd.read_excel(country_file_path, usecols=columns_to_read)

data_xl = []
row=1
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
            data_xl.append({'State': state_full_name, 'URL': url, 'Total': 0})
            print(f"State: {state_full_name}, URL: {url}, Total: {0}")
            row+=1

df = pd.DataFrame(data_xl)

output_excel_path = "output/business.xlsx"
df.to_excel(output_excel_path, index=False)
print("URLs saved to", output_excel_path)
