import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

print('hello')

# Define the scope
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive.file','https://www.googleapis.com/auth/drive']

# Add your service account file
creds = ServiceAccountCredentials.from_json_keyfile_name('cred.json', scope)

# Authorize the clientsheet 
client = gspread.authorize(creds)

# Get the instance of the Spreadsheet
sheet = client.open('Youtube Trending Videos')

# Get the first sheet of the Spreadsheet
sheet_instance = sheet.get_worksheet(0)

# Create a Pandas DataFrame
data = {'Name': ['John', 'Anna', 'Peter', 'Linda'],
        'Age': [23, 45, 35, 32],
        'Country': ['USA', 'Canada', 'Australia', 'Germany']}
df = pd.DataFrame(data)

# Export the DataFrame to Google Sheets
sheet_instance.insert_rows(df.values.tolist(), 2)