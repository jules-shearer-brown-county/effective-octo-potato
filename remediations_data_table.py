from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import utility, proccess_apps_team

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

results = utility.get_remediations()

df = utility.read_data(results)

grouped_by_severity = df[['hvm_id', 'vuln_id.severity']].groupby('vuln_id.severity')

counts = pd.concat([
    df['first_seen'].value_counts(),
    df['ack_dt'].value_counts().mul(-1),
    df['closed_dt'].value_counts().mul(-1)
])

counts.sort_index()
counts = counts.reset_index()

fig = go.Figure(go.Waterfall(
    x=counts.index,
    y=counts['count']
))

#PlotlyDataTable
def tbl():
    return dash_table.DataTable(
        df.to_dict('records'),
        columns= [{"name": i, "id": i, 'presentation': 'markdown'} if ((i=='host_id.link') | (i=='vuln_id.link')) else ({"name": i, "id": i}) for i in columns],
        page_action='native',
        sort_action='native',
        filter_action='native',
        sort_mode='multi',
        style_cell={
            'overflow':'hidden',
            'TextOverflow':'ellipsis',
            'maxWidth':'0'
        },
        page_size=20,
    )

app = Dash()
# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H4('Remediations'),
#    dcc.Graph(figure=fig),
    tbl(),
    html.Div(id='datatable-interactivity-containter')
])

if __name__ == '__main__':
    utility.open_dashboard_in_firefox()
    app.run(debug=True)
