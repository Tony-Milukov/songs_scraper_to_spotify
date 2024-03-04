import re


def getDate():
    # date regex YYYY-MM-DD:
    date_regex = r'(\d{4})-(\d{2})-(\d{2})'
    date = input("Select date, in format YYYY-MM-DD: ")

    # while the date is not YYYY-MM-DD
    while not re.match(date_regex, date):
        print("Invalid date format. Please use YYYY-MM-DD format.")
        date = input("Select date, in format YYYY-MM-DD: ")
    return date
