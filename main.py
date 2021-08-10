#####################################################################################
#                                                                                   #
# Overview                                                                          #
#                                                                                   #
#    main.py --worksheet="daily_stock_summary"                                      #
#                                                                                   #
# Description                                                                       #
#                                                                                   #
#    This script is used to validate the attributes of fields                       #
#    in a google sheets database.                                                   #
#                                                                                   #
# Implementation                                                                    #
#                                                                                   #
#    date        07-04-2021                                                         #
#    version     1.0.0                                                              #
#                                                                                   #
#####################################################################################

#####################
# Imports           #
#####################

import argparse
import datetime
import gspread
import logging

#####################
# Arguments         #
#####################

parser = argparse.ArgumentParser()

parser.add_argument('--worksheet', '-w', required=True, help='Google Worksheet')

args = parser.parse_args()

#####################
# Logging           #
#####################

log_date = datetime.date.today()

log_file = "google_sheets_validate_{}.log".format(log_date)

logging.basicConfig(format="%(asctime)s - %(filename)s - %(levelname)s - %(message)s", level=logging.INFO, filename=log_file)

#####################
# Functions         #
#####################

def create_connection():
    '''creates google sheets connection'''

    gs_conn = gspread.service_account('credentials.json')

    return gs_conn

def get_worksheet_values(gs_conn, wks_name):
    '''returns all values from a worksheets as a list of disctionaries'''

    try:

        wks = gs_conn.open(wks_name).sheet1

        values = wks.get_all_records()

    except (gspread.SpreadsheetNotFound) as E:

        logging.error(E)

    return values

#####################
# Main              #
#####################

def main():

    logging.info("Connecting to google sheets database.")

    gs_conn   = create_connection()

    wks_name  = args.worksheet

    values    = get_worksheet_values(gs_conn, wks_name)

    for V in values:

        # add validation logic here
        
        print(V)


#####################
# Start             #
#####################

if __name__ == '__main__':
    main()
    
