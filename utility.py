#!/bin/python

import os, subprocess, glob

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

def get_remediations():
    dir_name = "/mnt/c/Users/Jules.Shearer/Downloads/"
    files = glob.glob(dir_name + 'Remediated (2).xlsx')
    return max(files, key=os.path.getctime)
