import gspread
from oauth2client.service_account import ServiceAccountCredentials


# use creds to create a client to interact with the Google Drive API
scope = [   'https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('client-secret.json', scope)
client = gspread.authorize(creds)

# Find a workbook by name and open a sheet within it by name
spreadsheet = client.open("[VLDA] Server Tracking Management")
sheet = spreadsheet.worksheet("Script Sheet")

#Opens and overwrites servers.txt
file = open("servers.txt", "w")

# Extract and writes all of the values
list_of_hashes = sheet.get_all_values()
for line in list_of_hashes:
    if(line[0].strip() != ''): 
        file.write(line[0] + "," + line[1] + '\n')