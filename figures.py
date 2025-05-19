#!/bin/python
#figures.py module for holding the shared figures between reports
from dash import dash_table
import utility
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import datetime

def waterfall(df):
    counts=pd.concat([
        df.groupby(pd.Grouper(key='first_seen', freq='ME'))['hvm_id'].count(),
        df.groupby(pd.Grouper(key='ack_dt', freq='ME')).count()['hvm_id'].mul(-1),
        df.groupby(pd.Grouper(key='closed_dt', freq='ME')).count()['hvm_id'].mul(-1)
    ])
    last_year=counts[counts.index < datetime.datetime(2025,1,1)]
    counts = counts.drop(last_year.index)
    counts[datetime.datetime(2024,12,31)]=last_year.sum()
    counts=counts.sort_index(level=1)
    counts = pd.DataFrame(counts).reset_index()

    fig = go.Figure(go.Waterfall(
        x=[[i.strftime('%B, %Y') for i in counts['index']], counts.index],
        y=counts['hvm_id'],
        textposition='outside',
        textinfo='delta',
        showlegend=True,
        decreasing = {"marker":{"color":"green", "line":{"color":"black", "width":2}}},
        increasing = {"marker":{"color":"red"}},
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
