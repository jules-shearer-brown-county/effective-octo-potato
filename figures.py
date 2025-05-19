#!/bin/python
#figures.py module for holding the shared figures between reports
from dash import dash_table
import utility
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import datetime

def waterfall(df):
    counts = pd.concat([
        df['first_seen'].value_counts(),
        df['ack_dt'].value_counts().mul(-1),
        df['closed_dt'].value_counts().mul(-1)
    ], keys=['opened', 'acknowledged','closed'])
    last_year=counts.filter([i for i in counts.index if i[1] < datetime.date(2025,1,1)])
    counts = counts.drop(last_year.index)
    counts[('total',datetime.date(2024,12,31))]=last_year.sum()
    counts=counts.sort_index(level=1)

    counts = pd.DataFrame(counts).reset_index()

    fig = go.Figure(go.Waterfall(
        x=counts.index,
        y=counts['count']

    ))
    fig.update_layout(title="Vulnerability Discovery and Resolution")
    return fig



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
