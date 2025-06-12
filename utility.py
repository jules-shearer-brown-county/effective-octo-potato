#!/bin/python

import os, subprocess, glob
import pandas as pd

def add_apps(data):
    apps=pd.read_excel("/mnt/c/Users/jules.shearer/Downloads/names_and_tags.xlsx")
    data = data.merge(apps, how='left', on='host_id.hostname')
    return data

def get_remediations():
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    files = glob.glob(dir_name + 'vuln_remediation_export_*.xlsx')
    return max(files, key=os.path.getctime)


def get_hosts_export():
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    files = glob.glob(dir_name + 'hosts_export*.xlsx')
    return max(files, key=os.path.getctime)

def get_names_and_tags():
    file_name = "/mnt/c/Users/Jules.Shearer/Downloads/" + 'names_and_tags.xlsx'
    apps = pd.read_excel(file_name)
    return apps[apps['Application'].notna()]

def preprocess(data):
    data['first_seen'] = pd.to_datetime(data['first_seen'], unit='s')
    data['last_seen'] = pd.to_datetime(data['last_seen'], unit='s')
    data['vuln_id.severity']= data['vuln_id.severity'].replace({
        3:'Medium',
        4:'High',
        5:'Critical'})
    data['vuln_id.link'] = '[link](' + 'https://app.uncommonx.com/network-disc/vuln/' + data['vuln_id.vuln_id'].astype(str) +  ')'
    data['host_id.link'] = '[link](' + 'https://app.uncommonx.com/network-disc/host/' + data['host_id.host_id'].astype(str) +  ')'
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
    remediation_category = pd.CategoricalDtype(categories=['open', 'fixed', 'acknowledged', 'closed'])
    data["remediation_category"] = pd.Series('open', index=data.index, dtype='category')
    data["remediation_category"] = data["remediation_category"].astype(remediation_category)
    data.loc[data.ack_dt.notna(), 'remediation_category']='acknowledged'
    data.loc[data.closed_dt.notna() & data.ack_dt.isna(), 'remediation_category']='fixed'
    if 'ttr' in data.columns:
        data.loc[data.ack_dt.isna() & data.closed_dt.isna() & data.ttr.notna(), 'remediation_category']='closed'
    return data

def read_data(fileLocation):
    data = pd.read_excel(fileLocation)
    data = preprocess(data)
    return data

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

if __name__ ==  '__main__':

    data = pd.concat([read_data(get_remediations()), read_data(get_latest_scan_from_downloads())])

