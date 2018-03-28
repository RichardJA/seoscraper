import gspread
import page
from oauth2client.service_account import ServiceAccountCredentials


def upload_information(pages):
    """
    Is sent the information from the main file and uploads it row by row to the Google Doc
    """
    print(pages[0].page_url)
    """
    # Initialising connection to Google Sheets
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name('secret_file.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Technical SEO').sheet1

    print("Updating Spreadsheet")

    row = ['URL', 'Title Text', 'Title Length', 'Bad Anchor Text', 'No Alt Text', 'H1 Tags']
    title_list = sheet.range('A1:F1')
    for n in range(len(row)):
        title_list[n].value = row[n]

    sheet.update_cells(title_list)

    cell_list = sheet.range('A2:F1000')
    t = 0
    for x in range(len(pages)):
        for n in range(t, t + len(title_list), len(title_list)):
            cell_list[n].value = pages[x].page_url
            cell_list[n + 1].value = pages[x].title_text
            cell_list[n + 2].value = pages[x].title_length
            cell_list[n + 3].value = pages[x].anchors
            cell_list[n + 4].value = pages[x].alt_text['With Alt']
            cell_list[n + 5].value = pages[x].h_tags['h1']
        t += len(title_list)

    sheet.update_cells(cell_list)
    """
