#!/bin/python3
#proccess_apps_team.py - chops up a vuln export based on host_id.custom_tags

import pandas as pd
import proccess_apps_team
import utility


def prep():
    df = pd.concat([proccess_apps_team.proccess_apps_team(), proccess_apps_team.proccess_apps_team(utility.get_remediations()), proccess_apps_team.proccess_apps_team("/mnt/c/Users/jules.shearer/Downloads/brown_county_gov_vuln_rememdiation_365.xlsx")])
    df.sort_values(by=['last_seen'])
    df.drop_duplicates(subset='hvm_id', keep='first', inplace=True)
    df=df[df['Application'].notna()]
    df['Pending'] = pd.Series(dtype='string')
    df=df.rename(columns={'first_seen':'First Seen', 'last_seen':'Last Seen', 'vuln_id.name':'Name', 'vuln_id.severity':'Severity','host_id.hostname':'Host','host_id.link':'url','vuln_id.link':'Link' })
    df.to_excel("/mnt/c/Users/jules.shearer/Downloads/data0.xlsx")


if __name__ ==  '__main__':
    prep()
