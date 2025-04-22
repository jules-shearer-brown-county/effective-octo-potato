from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import read_data
import waterfall

df=read_data.read_data('/mnt/c/Users/jules.shearer/Downloads/brown_county_gov_vuln_rememdiation_365.xlsx')

app = Dash()

# Requires Dash 2.17.0 or later
app.layout = [
    dash_table.DataTable(
        df.to_dict('records'),
        style_cell={
            'overflow':'hidden',
            'textOverflow': 'ellipsis',
            'minWidth': '180px', 'width': '180px','maxWidth': '180px',
        },
        page_size=20,
        id='table',
    )
]

#@callback(
#    Output(component_id='table', component_property='figure'),
#    Input(component_id='hostname', component_property='value'),
#)
#
#def update_graph(col_chosen):
#    return fig
#
if __name__ == '__main__':
    app.run(debug=True)
