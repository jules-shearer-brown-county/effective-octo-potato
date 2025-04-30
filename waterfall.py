#!bin/python
#
import read_data
import sys, pyperclip
import pandas as pd
import plotly.graph_objects as go

def waterfall(deltas):
    fig = go.Figure(go.Waterfall(
        x = deltas['date'],
        textposition = "outside",
        y = deltas['count'],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
    fig.update_layout(
        title = "Ugly Graph",
        showlegend = True
    )
    fig.show()

def preprocess(data):
    make_negative=lambda x: 0-x
    deltas = pd.concat([data['first_seen'].value_counts(), data['closed_dt'].value_counts().apply(make_negative), data['ack_dt'].value_counts().apply(make_negative)])
    deltas = deltas.reset_index()
    deltas['date'] = deltas['index']
    deltas = deltas[['date', 'count']]
    deltas = deltas.sort_values(by='date')
    deltas=deltas.reset_index(drop=True)
    return deltas

if __name__ ==  '__main__':
    if len(sys.argv) > 1:
        # Get information from the command line
        fileLocation = ''.join(sys.argv[1:])
    else:
        #Get location from the clipboard
        fileLocation = pyperclip.paste()
    data = read_data.read_data(fileLocation)
    deltas = preprocess(data)
    waterfall(deltas)
