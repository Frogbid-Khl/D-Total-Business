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

# Test the function
if is_phone_number("tel:201-285-4922"):
    print("Phone Number")
else:
    print("Not Found")
