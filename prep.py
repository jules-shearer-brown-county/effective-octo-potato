#!/bin/python3
#proccess_apps_team.py - chops up a vuln export based on host_id.custom_tags

import pandas as pd
import proccess_apps_team
import utility


def prep():
    #Get the entire backlog of results and put it in one data frame
    df = pd.concat([proccess_apps_team.proccess_apps_team(), proccess_apps_team.proccess_apps_team(utility.get_remediations()), proccess_apps_team.proccess_apps_team("/mnt/c/Users/jules.shearer/Downloads/brown_county_gov_vuln_rememdiation_365.xlsx")])
    #sort the large data frame by last_seen
    df.sort_values(by=['last_seen'])
    #get rid of duplicates, keeping the most recent
    df.drop_duplicates(subset='hvm_id', keep='first', inplace=True)
    #Keep the values where there is not a null value in the column 'Applications'
    df=df[df['Application'].notna()]
    #Add a column "Pending" of type string
    df['Pending'] = pd.Series(dtype='string')
    #Rename a couple of columns
    df=df.rename(columns={'first_seen':'First Seen', 'last_seen':'Last Seen', 'vuln_id.name':'Name', 'vuln_id.severity':'Severity','host_id.hostname':'Host','host_id.link':'url','vuln_id.link':'Link' })
    #Write the entire dataframe to an excel file
    df.to_excel("/mnt/c/Users/jules.shearer/Downloads/data0.xlsx")


if __name__ ==  '__main__':
    prep()
