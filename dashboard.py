from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import proccess_apps_team
import utility

latest_scan = utility.get_latest_scan_from_downloads()
df=proccess_apps_team.proccess_apps_team(latest_scan)

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
    dash_table.DataTable(
        df.to_dict('records'),
        [{"name": i, "id": i} for i in df.columns],
        page_action='native',
        sort_action='native',
        filter_action='native',
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
