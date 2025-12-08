#!/bin/python3
#prep.py - Get the data ready for a report

import pandas as pd
import argparse, os
import process_apps_team
import utility

dir_name = "/mnt/c/Users/jules.shearer/Downloads/"

def prep(args):
    #Get the entire backlog of results and put it in one data frame
    df = pd.concat([process_apps_team.process_apps_team(),
                    process_apps_team.process_apps_team(utility.get_remediations()),
                    process_apps_team.process_apps_team(dir_name + "brown_county_gov_vuln_rememdiation_365.xlsx")])

    #sort the large data frame by last_seen
    df.sort_values(by=['last_seen'])

    #get rid of duplicates, keeping the most recent
    df.drop_duplicates(subset='hvm_id',
                       keep='first',
                       inplace=True)

    #Keep the values where there is not a null value in the column 'Applications'
    df=df[df['Application'].notna()]

    #Add a column "Pending" of type string
    df['Pending'] = ''

    #Rename a couple of columns
    df=df.rename(columns={'first_seen':'First Seen',
                          'last_seen':'Last Seen',
                          'vuln_id.name':'Name',
                          'vuln_id.severity':'Severity',
                          'host_id.hostname':'Host',
                          'host_id.link':'url',
                          'vuln_id.link':'Link' })

    #Write the entire dataframe to the file path specified in  or return the dataframe
    if(args.output_file):
        df.to_excel(args.output_file)
    else:
        return df

parser = argparse.ArgumentParser(
    prog="UncommonX report",
    description="Cleans the data from uncommonX and puts it in a format understandable by the unX report for the steering commitee",
    epilog="Good luck"
)

parser.add_argument("-o", "--output_file", default = "output_file.xlsx")

parser.add_argument("-d", "--working_directory", default=os.getcwd())

if __name__ ==  '__main__':

    args = parser.parse_args()

    prep(args)
