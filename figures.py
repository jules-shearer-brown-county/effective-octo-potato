#!/bin/python
#figures.py module for holding the shared figures between reports
from dash import dash_table
import utility
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def waterfall(df):
    counts = count_discovered_and_closed(df)

    fig = go.Figure(go.Waterfall(
        x=counts.index,
        y=counts
    ))
    return fig

def count_discovered_and_closed(df):
    counts = pd.concat([
        df['first_seen'].value_counts(),
        df['ack_dt'].value_counts().mul(-1),
        df['closed_dt'].value_counts().mul(-1)
    ])
    counts.index= pd.to_datetime(counts.index)
    counts = counts.resample('ME').sum()
    return counts


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

if __name__ == '__main__':
    df = utility.read_data(utility.get_remediations())
    utility.view(waterfall(df))
