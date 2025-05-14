#!/bin/python3
#proccess_apps_team.py - chops up a vuln export based on host_id.custom_tags

import pandas as pd
import sys, pyperclip, os, subprocess, datetime
import plotly.express as px

import utility


def print_results(data):
    print("Applications and their count of vulnerabilties")
    print(data.value_counts(subset=['Application','vuln_id.severity'], sort=False))

    print("Hosts and their count of vulnerabilties")
    grouped_by_hosts = data[['hvm_id', 'host_id.hostname']].groupby('host_id.hostname')
    print(grouped_by_hosts.count())

    print("discovery date and their count of vulnerabilties")
    grouped_by_first_seen_date = data[['hvm_id', 'first_seen_date']].groupby('first_seen_date')
    print(grouped_by_first_seen_date.count())

    print("Severity and their count of vulnerabilties")
    grouped_by_severity = data[['hvm_id', 'vuln_id.severity']].groupby('vuln_id.severity')
    print(grouped_by_severity.count())

    for i in range(datetime.datetime.now().month):
        firstseen_by_month = data[(data['first_seen'] > datetime.date(2024,i+1,1)) & (data['first_seen'] < datetime.date(2025,i+2,1))]
        print("%d for the %d month of the year" % (len(firstseen_by_month.index), i))

def proccess_apps_team(input_file=utility.get_latest_scan_from_downloads()):
    data = utility.read_data(input_file)

    apps = ['Human Services', 'Milestone','CCure', 'LandNAV', 'Papercut', 'OMS', 'Kronos', 'Pinnacle', 'New World', 'Laserfiche', 'AWS', 'County Law', 'Public Works', 'Misc']

    data['Application'] = pd.Series(dtype=str)
    for app_name in apps:
        data = data[data['host_id.custom_tags'].notna()]
        data.loc[data['host_id.custom_tags'].str.contains(app_name), 'Application'] = app_name

    return data

if __name__ ==  '__main__':

    data = proccess_apps_team()
    print_results(data)

print('EOF')
