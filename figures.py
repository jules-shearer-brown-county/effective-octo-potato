#!/bin/python
#figures.py module for holding the shared figures between reports
from dash import dash_table
from plotly.subplots import make_subplots
import utility
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
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
        decreasing = {"marker":{"color":"green", "line":{"color":"black", "width":2}}},
        increasing = {"marker":{"color":"red"}},
    ))
    fig.update_layout(title="Vulnerability Discovery and Resolution")
    return fig

def app_and_severity(df):
    fig = make_subplots(rows=1, cols=3, specs=[[{'type':'domain'},{'type':'domain'},{'type':'domain'} ]])
    fig.add_trace(pie_chart(df, 'vuln_id.severity'), 1,1)
    fig.add_trace(pie_chart(df, 'Application'), 1,2)
    fig.add_trace(pie_chart(df, 'remediation_category'), 1,3)
    fig.update_traces(textposition='inside', textinfo='percent+label+value')
    fig.update(layout_showlegend=False)
    return fig

def application_pie_chart(df):
    grouped_by_application = df.value_counts('Application')
    application_pie_chart= px.pie(
        grouped_by_application,
        names=grouped_by_application.index,
        values=grouped_by_application.values,
        title="Number of vulnerabilties, application as % of whole",
        color=grouped_by_application.index,
    )
    application_pie_chart.update_traces(textposition='inside', textinfo='percent+label+value' )
    return application_pie_chart

def severity_pie_chart(df):
    grouped_by_severity = df.value_counts('vuln_id.severity')
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
        values=grouped_by_severity.values,
        title="Number of vulnerabilties, severity as % of whole",
        color=grouped_by_severity.index,
        color_discrete_map={
            'Medium':'yellow',
            'High' : 'orange',
            'Critical':'red'}
    )
    severity_pie.update_traces(textposition='inside', textinfo='percent+label+value' )
    return severity_pie

def pie_chart(df, col):
    counts = df.value_counts(col, dropna=False)
    pie = go.Pie(
        labels=counts.index,
        values=counts.values,
        title= "Percent of whole for %s" % col,
        name=col,
        #color=counts.index
    )
    return pie

def workstation_coverage(count=1):
    Departments = ['ADMIN', 'ADRC', 'ADRC Public PC', 'AIRPORT (using different PC names)', 'CHILDSUPPORT', 'CORPCOUNSEL', 'COUNTYBOARD', 'COUNTYCLERK', 'COUNTYEXEC', 'CTC', 'DTF', 'FACILITIES', 'GOLF', 'HEALTH', 'HR', 'HUMANSERVICES', 'Human Services:  Economic Support', 'Highway Department', 'JAIL', 'LIBRARY', 'LWC', 'MEDEXAMINER', 'MUSEUM', 'PALS', 'PARKSMGMT', 'PORTRESREC', 'PSC', 'PUBLICWORKS', 'ROD Public', 'ROD', 'SHERIFF', 'SYBLEHOPP', 'TECHSERVICES', 'TREASURER', 'UWEXT', 'VETERANS', 'Zoo', 'Public ', 'Public CTC', 'Public Library(Full AZURE Join)', 'Public Museum', 'Sheriff Squad Card', 'Test Machines']
    title='Currently Scanning %s of %s departments'%(count, str(len(Departments)))
    fig = go.Figure(data=[go.Bar(y=[count])], layout_xaxis_range=[0,len(Departments)])
    fig.update_layout(
        title_text=title
    )
    return fig

def total_devices(data):
    px.bar(data)
    return fig

if __name__ == '__main__':
    fig = total_devices(267, 2489)
    fig.show(renderer='firefox')
