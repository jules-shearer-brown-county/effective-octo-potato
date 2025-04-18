#!/bin/python
#read_data.py --import the file into memory and do some light human readible changes

import sys
import pyperclip
import pandas as pd

def read_data(fileLocation):
    data = pd.read_excel(fileLocation)
    data['first_seen'] = pd.to_datetime(data['first_seen'], unit='s').dt.date
    data['last_seen'] = pd.to_datetime(data['last_seen'], unit='s').dt.date
    data['ack_dt'] = pd.to_datetime(data['ack_dt'], unit='s').dt.date
    data['closed_dt'] = pd.to_datetime(data['closed_dt'], unit='s').dt.date
    data['vuln_id.link'] = 'https://app.uncommonx.com/network-disc/vuln/' + data['vuln_id.unique_id'].astype(str)
    return data[['vuln_id.severity', 'vuln_id.name', 'host_id.hostname', 'host_id.ip_address', 'vuln_id.link', 'details.results', 'hvm_id', 'first_seen', 'last_seen', 'vuln_id.first_seen', 'vuln_id.last_seen','vuln_id.exploit']]

if __name__ ==  '__main__':
    if len(sys.argv) > 1:
        # Get information from the command line
        fileLocation = ''.join(sys.argv[1:])
    else:
        #Get location from the clipboard
        fileLocation = pyperclip.paste()

    read_data(fileLocation)
