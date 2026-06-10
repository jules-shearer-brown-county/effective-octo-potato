#!/bin/python3
#prep.py - Get the data ready for a report

import pandas as pd
import sys
import argparse
import proccess_apps_team
import utility

def prep():
    parser = argparse.ArgumentParser()

    parser.add_argument( "vulnerabilities", help="path to the vuln_mapping_export.xlsx file")
    parser.add_argument( "remediations", help="path to the remediation_mapping_export.xlsx file")
    parser.add_argument( "deduplicated", help="path to the deduplicated.xlsx file")

    parser.add_argument( "-o", "--output", help="path to the output folder location")

    args = parser.parse_args()

    df = pd.concat([utility.read_data(args.vulnerabilities), utility.read_data(args.remediations)])

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

    df = pd.concat([df, pd.read_excel(args.deduplicated)])

    #sort the large data frame by last_seen
    df = df.sort_values(by=['Last Seen'])

    #get rid of duplicates, keeping the most recent
    df.drop_duplicates(subset='hvm_id', keep='last', inplace=True)

    #Keep the values where there is not a null value in the column 'Applications'
    df=df[df['Application'].notna()]

    #Write the entire dataframe to the file path specified in  or return the dataframe
    if(args.output):
        df.to_excel(args.output)
    else:
        return df

if __name__ ==  '__main__':

    prep()
