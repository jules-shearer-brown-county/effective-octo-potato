#!/bin/python3
#prep.py - Get the data ready for a report

import pandas as pd
import sys
import argparse
import utility

def prep():
    parser = argparse.ArgumentParser(
        description="Preparation for deduplicating data for the UncommonX report",
        epilog="If a needed file is not specified it will search for one matching the naming pattern in the directory .prep is run from")

    parser.add_argument("-v",
                        "--vulnerabilities",
                        default=utility.get_latest_vuln_mapping(),
                        help="path to the vuln_mapping_export.xlsx file")

    parser.add_argument("-r",
                        "--remediations",
                        default=utility.get_latest_remediation(),
                        help="path to the remediation_mapping_export.xlsx file")

    parser.add_argument("-d",
                        "--deduplicated",
                        default=utility.get_latest_deduplicated(),
                        help="path to the deduplicated.xlsx file")

    parser.add_argument("-n",
                        "--names_and_tags",
                        default=utility.get_names_and_tags(),
                        help="path to the names and tags.xlsx file")

    parser.add_argument( "-o",
                        "--output",
                        default="output.xlsx",
                        help="path to the output folder location")

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

    #Keep the values where there is not a null value in the column 'Applications'
    df=df[df['Application'].notna()]

    #sort the large data frame by last_seen
    df = df.sort_values(by=['Last Seen'])

    #get rid of duplicates, keeping the most recent
    df.drop_duplicates(subset='hvm_id', keep='last', inplace=True)

    #Write the entire dataframe to the file path specified in  or return the dataframe
    if(args.output):
        df.to_excel(args.output)
    else:
        df.to_excel(args.deduplicated)

if __name__ ==  '__main__':

    prep()
