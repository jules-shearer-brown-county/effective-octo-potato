#!/bin/python

import os, subprocess, glob
import pandas as pd

def read_data(fileLocation):
    data = pd.read_excel(fileLocation)
    data['first_seen'] = pd.to_datetime(data['first_seen'], unit='s').dt.date
    data['last_seen'] = pd.to_datetime(data['last_seen'], unit='s').dt.date
    data['closed_dt'] = pd.to_datetime(data['closed_dt'], unit='s').dt.date
    data['vuln_id.link'] = '[link](' + 'https://app.uncommonx.com/network-disc/vuln/' + data['vuln_id.vuln_id'].astype(str) +  ')'
    data['host_id.link'] = '[link](' + 'https://app.uncommonx.com/network-disc/host/' + data['host_id.host_id'].astype(str) +  ')'
    if( 'ack_dt' in data.columns ):
        data['ack_dt'] = pd.to_datetime(data['ack_dt'], unit='s').dt.date
    return data.drop(columns=[col for col in data if data[data[col].notna()].empty])

def open_file_in_browser(html_path):
    current_dir = os.getcwd()
    absolute_wsl_path = os.path.join(current_dir, html_path)
    windows_path = subprocess.check_output(["wslpath", "-w", absolute_wsl_path]).decode().strip()
    subprocess.run(["/mnt/c/Program Files/Mozilla Firefox/firefox.exe", windows_path])

def open_dashboard_in_firefox():
    subprocess.run(["/mnt/c/Program Files/Mozilla Firefox/firefox.exe",'http://localhost:8050'])

def open_in_browser(windows_path):
    subprocess.run(["/mnt/c/Program Files/Mozilla Firefox/firefox.exe", windows_path])

def view(fig):
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    os.makedirs(dir_name,exist_ok=True)
    fig_name = 'plot.html'
    html_path = os.path.join(dir_name, fig_name)
    fig.write_html(html_path)
    open_file_in_browser(html_path)

def get_latest_scan_from_downloads():
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    files = glob.glob(dir_name + 'vuln_mapping_export*.xlsx')
    return max(files, key=os.path.getctime)

def get_file_path_for_all_scans_from_downloads():
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    files = glob.glob(dir_name + 'vuln_mapping_export*.xlsx')
    return [read_data(i) for i in files]

def unique_scans_results():
    scans = pd.concat(get_file_path_for_all_scans_from_downloads())
    return scans.sort_values('last_seen').drop_duplicates(subset=['hvm_id'], keep='last')

def get_remediations():
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    files = glob.glob(dir_name + 'Remediated (2).xlsx')
    return max(files, key=os.path.getctime)

def get_names_and_tags():
    file_name = "/mnt/c/Users/Jules.Shearer/Downloads/" + 'names_and_tags.xlsx'
    apps = pd.read_excel(file_name)
    return apps[apps['Application'].notna()]
