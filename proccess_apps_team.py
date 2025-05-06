#!/bin/python3
#proccess_apps_team.py - chops up a vuln export based on host_id.custom_tags

import pandas as pd
import sys, pyperclip, os, subprocess
import plotly.express as px

def open_in_browser(html_path):
    current_dir = os.getcwd()
    absolute_wsl_path = os.path.join(current_dir, html_path)
    windows_path = subprocess.check_output(["wslpath", "-w", absolute_wsl_path]).decode().strip()
    subprocess.run(["/mnt/c/Program Files/Mozilla Firefox/firefox.exe", windows_path])

def view(fig):
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    os.makedirs(dir_name,exist_ok=True)
    fig_name = 'plot.html'
    html_path = os.path.join(dir_name, fig_name)
    fig.write_html(html_path)
    open_in_browser(html_path)

def proccess_apps_team(input_file):
    data = pd.read_excel(input_file)

    apps = ['Milestone','CCure', 'LandNAV', 'Papercut', 'v-as400-data', 'OMS', 'Kronos', 'Pinnacle', 'New World', 'Laserfiche', 'AWS', 'County Law']

    data['Application'] = pd.Series(dtype=str)
    for app_name in apps:
        data = data[data['host_id.custom_tags'].notna()]
        data.loc[data['host_id.custom_tags'].str.contains(app_name), 'Application'] = app_name
    return data

if __name__ ==  '__main__':
    if len(sys.argv) > 1:
        input_file =''.join(sys.argv[1:])
    else:
        input_file = "/mnt/c/Users/Jules.Shearer/Downloads/vuln_mapping_export_1745957589285.xlsx"
        #input_file = pyperclip.paste()

    data = proccess_apps_team(input_file)
    grouped_by_application = data[['hvm_id', 'Application']].groupby('Application')
    print("Applications and their count of vulnerabilties")
    print(grouped_by_application.count())

    print("Hosts and their count of vulnerabilties")
    grouped_by_hosts = data[['hvm_id', 'host_id.hostname']].groupby('host_id.hostname')
    print(grouped_by_hosts.count())

    print("discovery date and their count of vulnerabilties")
    grouped_by_first_seen_date = data[['hvm_id', 'first_seen_date']].groupby('first_seen_date')
    print(grouped_by_first_seen_date.count())

    print("Severity and their count of vulnerabilties")
    grouped_by_severity = data[['hvm_id', 'vuln_id.severity']].groupby('vuln_id.severity')
    print(grouped_by_severity.count())
    app = grouped_by_severity.count()
    app.rename(
            index={
                3:'Medium',
                4:'High',
                5:'Critical'
            },
            inplace=True),

    severity_pie = px.pie(
        app,
        names=app.index,
        values='hvm_id',
        title="Number of vulnerabilties severity as % of whole"
    )
    view(severity_pie)

print('EOF')
