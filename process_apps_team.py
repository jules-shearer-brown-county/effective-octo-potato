#!/bin/python3
#processAppsTeam.py - chopps up a vuln export based on host_id.custom_tags

import pandas as pd
import sys, pyperclip

if len(sys.argv) > 1:
    input_file =''.join(sys.argv[1:])
else:
    input_file = "/mnt/c/Users/Jules.Shearer/Downloads/vuln_mapping_export_1744811551431.xlsx"
    #input_file = pyperclip.paste()

def process_apps_team(input_file):
    data = pd.read_excel(input_file)
    data=data[data['host_id.custom_tags'].notna()]
    #data=data[data['host_id.custom_tags'].str.contains('Apps Team')]
    data=data[data['vuln_id.severity']>=5]

    Apps = ['Milestone','CCure', 'LandNAV', 'Papercut', 'v-as400-data', 'OMS', 'Kronos', 'Pinnacle', 'New World', 'Laserfiche', 'AWS']

    with pd.ExcelWriter('/mnt/c/Users/Jules.Shearer/Downloads/vulnerability_by_application.xlsx', engine='xlsxwriter') as writer:
        for app in Apps:
            vulns = data[data['host_id.custom_tags'].str.contains(app)]
            print("found %d in %s" % (len(vulns.index), app))
            vulns.to_excel(writer, sheet_name=app, index=False)

process_apps_team(input_file)

print('EOF')
