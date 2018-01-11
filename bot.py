from config import *
from gdocument import GDocument


def main():
    spreadsheet = GDocument(spreadsheet_id=CONSTANTS['SPREADSHEET_ID'])

    result = spreadsheet.write_expense("Nuovo Test", 15.5)
    print(result)


if __name__ == '__main__':
    main()
