from __future__ import print_function
import gspread
from oauth2client.client import SignedJwtAssertionCredentials
import pandas as pd
import json

SCOPE = ["https://spreadsheets.google.com/feeds"]
SECRETS_FILE = "Pbpython-9c80d2999710.json"
SPREADSHEET = "PBPython User Survey (Responses)"

json_key = json.load(open(SECRETS_FILE))
# Authenticate using the signed key
credentials = SignedJwtAssertionCredentials(json_key['client_email'],
                                            json_key['private_key'], SCOPE)

gc = gspread.authorize(credentials)
workbook = gc.open(SPREADSHEET)
# Get the first sheet
sheet = workbook.sheet1
data = pd.DataFrame(sheet.get_all_records())

column_names = {'Timestamp': 'timestamp',
                'do you want to help': 'help',
                }
data.rename(columns=column_names, inplace=True)
data.timestamp = pd.to_datetime(data.timestamp)
print(data.head())