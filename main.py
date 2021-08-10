#####################################################################################
#                                                                                   #
# Overview                                                                          #
#                                                                                   #
#    main.py --schema="stocks_schema.json "--worksheet="daily_stocks_summary"       #
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
import collections
import datetime
import gspread
import json
import logging

#####################
# Arguments         #
#####################

parser = argparse.ArgumentParser()

parser.add_argument('--schema', '-s', required=True, help='Database Schema')

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

def import_schema(file_name):
    '''imports database schema'''

    data = None

    try:
        with open(file_name) as contents:

            data = json.load(contents, object_pairs_hook=collections.OrderedDict)

    except (IOError) as E:

        print("Error: {}".format(E))

    return data

def create_connection():
    '''creates google sheets connection'''

    gs_conn = gspread.service_account('credentials.json')

    return gs_conn

def get_worksheet_values(gs_conn, wks_name):
    '''returns all values from a worksheet as a list of disctionaries'''

    try:

        wks = gs_conn.open(wks_name).sheet1

        values = wks.get_all_records()

    except (gspread.SpreadsheetNotFound) as E:

        logging.error(E)

    return values

def check_int(field, value):
    '''checks if the field is an integer'''

    if isinstance(value, int):
        pass

    else:
        value_error(field, value)

def check_string(field, value, length):
    '''checks if the field length exceeds the expected length of characters'''

    if len(value) <= length:
        pass

    else:
        value_error(field, value)
        
def value_error(field, value):
    '''logs as error if a value does not match the field specifications as listed in the database schema'''

    logging.error("invalid value detected for column {}: \'{}\'".format(field, value))
    
#####################
# Main              #
#####################

def main():

    logging.info("Connecting to google sheets database.")

    schema    = import_schema(args.schema)
    
    gs_conn   = create_connection()

    wks_name  = args.worksheet

    values    = get_worksheet_values(gs_conn, wks_name)

    for table in schema:
        
        logging.info("Running checks for table {}".format(table))

        columns = list(schema[table])
        
            for V in values:

            # add validation logic here
        
                print(V)


#####################
# Start             #
#####################

if __name__ == '__main__':
    main()
    
