import gspread
from oauth2client.service_account import ServiceAccountCredentials


def connect_to_google_sheets():
    """
    Opens the connection to the shet and returns it
    """
    scope = ['https://www.googleapis.com/auth/spreadsheets']
    creds = ServiceAccountCredentials.from_json_keyfile_name('secret_file.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open('Technical SEO').sheet1

    # Calls the function to add the headers to the sheet
    add_headers(sheet)
    return sheet


def add_headers(sheet):
    """
    Adds the heads to the google sheet
    """
    row = ['URL', 'Title Text', 'Title Length', 'Bad Anchor Text', 'No Alt Text', 'H1 Tags', "Reading Score"]
    title_list = sheet.range('A1:G1')
    for n in range(len(row)):
        title_list[n].value = row[n]

    sheet.update_cells(title_list)


def upload_information(sheet, page, row):
    """
    Is sent the information from the main file and uploads it row by row to the Google Doc
    """
    cell_selection = "A" + str(row + 1) + ":G" + str(row + 1)
    cell_list = sheet.range(cell_selection)
    cell_data = [page.page_url, page.title_text, page.title_length, page.anchors, page.alt_text['Without Alt'],
                 page.h_tags['h1'], page.reading_score]

    for enum, data in enumerate(cell_data):
        cell_list[enum].value = data

    sheet.update_cells(cell_list)