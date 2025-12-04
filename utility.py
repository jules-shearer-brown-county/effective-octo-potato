#!/bin/python

import os, glob
import pandas as pd

dir_name = "/mnt/c/users/jules.shearer/Downloads/"

def add_apps(data):
    apps=pd.read_excel(dir_name + "/names_and_tags.xlsx")
    data = data.merge(apps, how='left', on='host_id.hostname')
    return data

def get_remediations():
    files = glob.glob(dir_name + 'vuln_remediation_export_*.xlsx')
    return max(files, key=os.path.getctime)

def get_hosts_export():
    files = glob.glob(dir_name + 'hosts_export*.xlsx')
    return max(files, key=os.path.getctime)

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
    data.loc[data.ack_dt.notna(), 'Category']='Acknowledged'
    data.loc[data.closed_dt.notna() & data.ack_dt.isna(), 'Category']='Remediated'
    return data

def get_latest_scan_from_downloads():
    files = glob.glob(dir_name + 'vuln_mapping_export*.xlsx')
    return max(files, key=os.path.getctime)

def read_data(fileLocation=get_latest_scan_from_downloads()):
    data = pd.read_excel(fileLocation)
    data = preprocess(data)
    return data

def get_file_path_for_all_scans_from_downloads():
    files = glob.glob(dir_name + 'vuln_mapping_export*.xlsx')
    return [read_data(i) for i in files]

def unique_scans_results():
    scans = pd.concat(get_file_path_for_all_scans_from_downloads())
    return scans.sort_values('last_seen').drop_duplicates(subset=['hvm_id'], keep='last')

if __name__ ==  '__main__':
    print(pd.concat([read_data(get_remediations()), read_data(get_latest_scan_from_downloads())]))
