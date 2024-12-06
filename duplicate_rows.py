import pandas as pd
from fuzzywuzzy import fuzz
import csv

# Read the CSV file
input_file = "/Users/micah/build/firstlove/data/Lead.csv"
unique_file = "unique_rows.csv"
duplicates_file = "duplicate_rows.csv"

# Define similarity threshold for "similar" comments__c
similarity_threshold = 80  # Adjust as needed (80 is generally considered a reasonable match threshold)

# Load the data
# df = pd.read_csv(input_file, encoding='ISO-8859-1')
df = pd.read_csv(input_file, encoding='unicode_escape')

# Convert NaN values in 'comments__c' to an empty string
df['comments__c'] = df['comments__c'].fillna("")
df['PostalCode'] = df['PostalCode'].fillna("")

# Prepare lists to store unique and duplicate rows
unique_rows = []
duplicate_rows = []

# Function to check similarity of comments__c
def is_similar(desc1, desc2, threshold=similarity_threshold):
    # Ensure both comments__c are strings
    if not isinstance(desc1, str) or not isinstance(desc2, str):
        return False
    return fuzz.ratio(desc1, desc2) >= threshold

# Loop over each row and check for duplicates
processed_emails = {}  # Dictionary to store already processed emails and comments__c
processed_records = {}

for _, row in df.iterrows():
    email = row['Email']
    postalcode =  row['PostalCode']
    comments = row['comments__c']

    key = (email, postalcode) if postalcode else email
    
    # Check if email already exists in the processed_emails dictionary
    if email in processed_emails:
        # Check for similar comments__c within processed_emails for this email
        found_duplicate = False
        for processed_desc in processed_emails[email]:
            if is_similar(comments, processed_desc):
                # If similar, add this row to duplicates
                duplicate_rows.append(row)
                found_duplicate = True
                break
        # If no similar description found, add it to unique and update the dictionary
        if not found_duplicate:
            unique_rows.append(row)
            processed_emails[email].append(comments)
    else:
        # If this is the first time seeing the email, add it as unique and initialize the description list
        unique_rows.append(row)
        processed_emails[email] = [comments]

# # Check if the key already exists in the processed_records dictionary
#     if key in processed_records:
#         # Check for similar descriptions within processed_records for this key
#         found_duplicate = False
#         for processed_desc in processed_records[key]:
#             if is_similar(comments, processed_desc):
#                 # If similar, add this row to duplicates
#                 duplicate_rows.append(row)
#                 found_duplicate = True
#                 break
#         # If no similar description found, add it to unique and update the dictionary
#         if not found_duplicate:
#             unique_rows.append(row)
#             processed_records[key].append(comments)
#     else:
#         # If this is the first time seeing this key, add it as unique and initialize the description list
#         unique_rows.append(row)
#         processed_records[key] = [comments]

# Convert lists to DataFrames
df_unique = pd.DataFrame(unique_rows)
df_duplicates = pd.DataFrame(duplicate_rows)

# Save unique and duplicate rows to separate CSV files
df_unique.to_csv(unique_file, index=False, quoting=csv.QUOTE_ALL)
df_duplicates.to_csv(duplicates_file, index=False, quoting=csv.QUOTE_ALL)

print(f"Unique rows saved to {unique_file}")
print(f"Duplicate rows saved to {duplicates_file}")