from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import utility, proccess_apps_team, figures

columns_to_show=[
    'last_seen',
    #'first_seen',
    #''ack_dt',
    'ack_by',
    #'closed_dt',
    'closed_by',
    #''details.type',
    #''details.results',
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

df = utility.read_data(utility.get_remediations())

app = Dash()
# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H4('Remediations'),
    dcc.Graph(figure=figures.waterfall(df)),
    figures.tbl(df, columns_to_show),
    html.Div(id='datatable-interactivity-containter')
])

if __name__ == '__main__':
    utility.open_dashboard_in_firefox()
    app.run(debug=True)
