#!/bin/python
#datatable.py module for holding the shared datatables between reports
import plotly.graph_objects as go
import pandas as pd
import utility

df = pd.concat([utility.read_data(utility.get_remediations()), utility.read_data(utility.get_latest_scan_from_downloads())])

fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                                    fill_color='paleturquoise',
                                    align='left'),
        cells=dict(values=df,
                                  fill_color='lavender',
                                  align='left')
)
                      ])

fig.show(renderer='firefox.exe')
