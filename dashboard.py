from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import proccess_apps_team
import utility, figures

apps = [
    'Human Services',
    'Milestone','CCure',
    'LandNAV',
    'Papercut',
    'OMS',
    'Kronos',
    'Pinnacle',
    'New World',
    'Laserfiche',
    'AWS',
    'County Law',
    'Public Works',
    'Misc']

columns=[
    'first_seen',
    'last_seen',
    'ack_dt',
    'ack_by',
    'closed_dt',
    'closed_by',
    'details.type',
    'details.results',
    #'vuln_id.vuln_id',
    'vuln_id.name',
    'vuln_id.severity',
    #'vuln_id.unique_id',
    #'vuln_id.first_seen',
    #'vuln_id.last_seen',
    'vuln_id.cve',
    'vuln_id.exploit',
    #'host_id.host_id',
    'host_id.hostname',
    #'host_id.ip_address',
    #'host_id.risk_score',
    #'host_id.criticality',
    #'ttr',
    'vuln_id.link',
    'host_id.link']

latest_scan = utility.get_latest_scan_from_downloads()

df = proccess_apps_team.proccess_apps_team(latest_scan)

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H4('Vulnerabilites'),
    dcc.Graph(figure=figures.severity_pie_chart(df)),
    html.Div(id='datatable-interactivity-containter'),
    dcc.Dropdown(id='Application',
                 options=apps,
                 value='CCure'),
])

if __name__ == '__main__':
    utility.open_dashboard_in_firefox()
    app.run(debug=True)
