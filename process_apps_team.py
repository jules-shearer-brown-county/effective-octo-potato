#!/bin/python3
#processAppsTeam.py - chops up a vuln export based on host_id.custom_tags

import pandas as pd
import sys, pyperclip

if len(sys.argv) > 1:
    input_file =''.join(sys.argv[1:])
else:
    input_file = "/mnt/c/Users/Jules.Shearer/Downloads/vuln_mapping_export_1745957589285.xlsx"
    #input_file = pyperclip.paste()

def process_apps_team(input_file):
    data = pd.read_excel(input_file)
    total_count = len(data.index)
    data=data[data['host_id.custom_tags'].notna()]
    #data=data[data['host_id.custom_tags'].str.contains('Apps Team')]
    #data=data[data['vuln_id.severity']>=5]

    Apps = ['Milestone','CCure', 'LandNAV', 'Papercut', 'v-as400-data', 'OMS', 'Kronos', 'Pinnacle', 'New World', 'Laserfiche', 'AWS', 'County Law']

    with pd.ExcelWriter('/mnt/c/Users/Jules.Shearer/Downloads/vulnerability_by_application.xlsx', engine='xlsxwriter') as writer:
        count = 0
        for app in Apps:
            vulns = data[data['host_id.custom_tags'].str.contains(app)]
            count += len(vulns.index)
            print("found %d in %s" % (len(vulns.index), app))
            vulns.to_excel(writer, sheet_name=app, index=False)
        print("found %d in %d records" % (count, total_count))

process_apps_team(input_file)

print('EOF')
