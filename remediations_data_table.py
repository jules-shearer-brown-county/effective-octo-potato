from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import read_data, utility, proccess_apps_team

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

df = read_data.read_data(results)

grouped_by_severity = df[['hvm_id', 'vuln_id.severity']].groupby('vuln_id.severity')

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    html.H4('Remediations'),
    dcc.Graph(figure=severity_pie_chart(grouped_by_severity.count())),
    dash_table.DataTable(
        df.to_dict('records'),
        [{"name": i, "id": i} for i in df.columns],
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
    ),
    html.Div(id='datatable-interactivity-containter')
])

if __name__ == '__main__':
    utility.open_dashboard_in_firefox()
    app.run(debug=True)
