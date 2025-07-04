#!/bin/python3
#proccess_apps_team.py - chops up a vuln export based on host_id.custom_tags

import pandas as pd
import sys, pyperclip, os, subprocess, datetime
import plotly.express as px

import utility


def print_results(data):
    print("Applications and their count of vulnerabilties")
    print(data.value_counts(subset=['Application','vuln_id.severity'], sort=False))

    print("Applications and their count of unique critical vulnerabilties")
    counts=data.value_counts(subset=['Application','vuln_id.vuln_id','vuln_id.severity'], sort=False)
    print(counts.xs('Critical', level='vuln_id.severity').to_frame().value_counts(subset='Application'))

    print("Hosts and their count of vulnerabilties")
    grouped_by_hosts = data[['hvm_id', 'host_id.hostname']].groupby('host_id.hostname')
    print(grouped_by_hosts.count())

    print("discovery date and their count of vulnerabilties")
    grouped_by_first_seen_date = data[['hvm_id', 'first_seen']].groupby('first_seen')
    print(grouped_by_first_seen_date.count())

    print("Severity and their count of vulnerabilties")
    grouped_by_severity = data[['hvm_id', 'vuln_id.severity']].groupby('vuln_id.severity')
    print(grouped_by_severity.count())


def proccess_apps_team(input_file=utility.get_latest_scan_from_downloads()):
    vulnerabilites = utility.read_data(input_file)
    return vulnerabilites

if __name__ ==  '__main__':
    open_vuln = proccess_apps_team()
    resolved_vuln = utility.read_data(utility.get_remediations())
    print_results(open_vuln)
