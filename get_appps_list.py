#! /bin/python

import asyncio
import configparser
from msgraph import GraphServiceClient
import pyperclip


if __name__ ==  '__main__':

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg', 'config.dev.cfg'])
    azure_settings = config['azure']

    graph: Graph = Graph(azure_settings)

    if len(sys.argv) > 1:
        #TODO: get list parameters from cmd
        list_id = 'C90FE204-A61E-4595-B29D-4AF82E686FA4'
        #list_id = ''.join(sys.argv[1:])
    else:
        #TODO: Get list ID from the clipboard
        list_id = pyperclip.paste()
