#!/bin/python
#read_data.py --import the file into memory and do some light human readible changes

import sys
import pyperclip
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

if __name__ ==  '__main__':
    read_data(fileLocation)
