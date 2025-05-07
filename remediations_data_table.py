from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import read_data

df=read_data.read_data('/mnt/c/Users/jules.shearer/Downloads/brown_county_gov_vuln_rememdiation_365.xlsx')

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = html.Div([
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
    app.run(debug=True)
