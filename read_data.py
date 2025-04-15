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
    return data

if __name__ ==  '__main__':
    if len(sys.argv) > 1:
        # Get information from the command line
        fileLocation = ''.join(sys.argv[1:])
    else:
        #Get location from the clipboard
        fileLocation = pyperclip.paste()

    read_data(fileLocation)
