from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import proccess_apps_team
import utility

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

def severity_pie_chart(grouped_by_severity):
    grouped_by_severity.rename(
            index={
                3:'Medium',
                4:'High',
                5:'Critical'
            },
            inplace=True),
    severity_pie = px.pie(
        grouped_by_severity,
        names=grouped_by_severity.index,
        values='hvm_id',
        title="Number of vulnerabilties severity as % of whole",
        color=grouped_by_severity.index,
        color_discrete_map={
            'Medium':'yellow',
            'High' : 'orange',
            'Critical':'red'}
    )
    severity_pie.update_traces(textposition='inside', textinfo='percent+label' )
    return severity_pie

latest_scan = utility.get_latest_scan_from_downloads()

df = proccess_apps_team.proccess_apps_team(latest_scan)

grouped_by_severity = df[['hvm_id', 'vuln_id.severity']].groupby('vuln_id.severity')

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H4('Vulnerabilites'),
    #dcc.Graph(figure=severity_pie_chart(grouped_by_severity.count())),
    dash_table.DataTable(
        df.to_dict('records'),
        columns= [{"name": i, "id": i, 'presentation': 'markdown'} if ((i=='host_id.link') | (i=='vuln_id.link')) else ({"name": i, "id": i}) for i in columns],
        page_action='native',
        style_cell={
            'overflow':'hidden',
            'TextOverflow':'ellipsis',
            'maxWidth':'0'
        },
        page_size=25,
    ),
    html.Div(id='datatable-interactivity-containter'),
    dcc.Dropdown(id='Application',
                 options=apps,
                 value='CCure'),
])

if __name__ == '__main__':
    utility.open_dashboard_in_firefox()
    app.run(debug=True)
