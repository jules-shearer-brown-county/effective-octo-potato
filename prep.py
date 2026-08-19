#!/bin/python3
#prep.py - Get the data ready for a report

import datetime as dt
import os, glob
import pandas as pd
import sys
import argparse

def get_latest(filename):
    files = glob.glob(filename)
    return max(files, key=os.path.getctime)

def add_apps(data):
    apps=pd.read_excel("names_and_tags.xlsx")
    data = data.merge(apps, how='left', on='host_id.hostname')
    return data

def preprocess(data):
    data['first_seen'] = pd.to_datetime(data['first_seen'], unit='s')
    data['last_seen'] = pd.to_datetime(data['last_seen'], unit='s')
    data['vuln_id.severity']= data['vuln_id.severity'].replace({
        3:'Medium',
        4:'High',
        5:'Critical'})
    data['vuln_id.link'] = 'https://app.uncommonx.com/network-disc/vuln/' + data['vuln_id.vuln_id'].astype(str)
    data['host_id.link'] = 'https://app.uncommonx.com/network-disc/host/' + data['host_id.host_id'].astype(str)
    if( 'ack_dt' in data.columns ):
        data['ack_dt'] = pd.to_datetime(data['ack_dt'], unit='s')
    if( 'ttr' in data.columns ):
        data['closed_dt'] = data['first_seen'] + pd.to_timedelta(data['ttr'], unit='d')
    else:
        data['closed_dt'] = pd.to_datetime(data['closed_dt'], unit='s')
    data = add_apps(data)
    data = assign_status(data)
    return data.drop(columns=[col for col in data if data[data[col].notna()].empty])

def assign_status(data):
    remediation_category = pd.CategoricalDtype(categories=['Open', 'Remediated', 'Acknowledged', 'Closed'])
    data["Category"] = pd.Series('Open', index=data.index, dtype='category')
    data["Category"] = data["Category"].astype(remediation_category)
    data.loc[(data['last_seen'] < (dt.datetime.now()-dt.timedelta(days=90))), 'Category']='Closed'
    data.loc[data['ack_dt'].notna(), 'Category']='Acknowledged'
    data.loc[data['closed_dt'].notna(), 'Category']='Remediated'
    return data

def read_data(fileLocation):
    data = pd.read_excel(fileLocation)
    return preprocess(data)

def prep():
    parser = argparse.ArgumentParser(
        description="Preparation for deduplicating data for the UncommonX report",
        epilog="If a needed file is not specified it will search for one matching the naming pattern in the directory .prep is run from")

    parser.add_argument("-v",
                        "--vulnerabilities",
                        default=get_latest('vuln_mapping_export_*.xlsx'),
                        help="path to the vuln_mapping_export.xlsx file")

    parser.add_argument("-r",
                        "--remediations",
                        default=get_latest('vuln_mapping_export_*.xlsx'),
                        help="path to the remediation_mapping_export.xlsx file")

    parser.add_argument("-d",
                        "--deduplicated",
                        default='deduplicated.xlsx',
                        help="path to the deduplicated.xlsx file")

    parser.add_argument("-n",
                        "--names_and_tags",
                        default=get_latest('names_and_tags.xlsx'),
                        help="path to the names and tags.xlsx file")

    parser.add_argument( "-o",
                        "--output",
                        default="output.xlsx",
                        help="path to the output folder location")

    args = parser.parse_args()

    #Read the data
    df = pd.concat([read_data(args.vulnerabilities), read_data(args.remediations)])

    df = pd.concat([df, pd.read_excel(args.deduplicated)])

    df = df[['hvm_id', 'last_seen', 'vuln_id.name', 'vuln_id.severity', 'host_id.hostname','host_id.link', 'vuln_id.link', 'Category', 'closed_dt', 'ack_dt', 'Application', 'first_seen', 'details.results']]

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

    #Keep the values where there is not a null value in the column 'Applications'
    df=df[df['Application'].notna()]

    #sort the large data frame by last_seen
    df = df.sort_values(by=['Last Seen'])

    #get rid of duplicates, keeping the most recent
    df.drop_duplicates(subset='hvm_id', keep='last', inplace=True)

    #Write the entire dataframe to the file path specified in  or return the dataframe
    df.to_excel(args.output)

if __name__ ==  '__main__':

    prep()
