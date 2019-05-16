import os
import sys
sys.path.insert(0, os.path.realpath(os.path.dirname(__file__)))
os.chdir(os.path.realpath(os.path.dirname(__file__)))
import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
import sqlite3
import pandas as pd

# Initialize the app
app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
# Connect to DB
conn = sqlite3.connect('twitter.db', check_same_thread=False)
# Token for the mapbox
mapbox_access_token = 'INSERT MAP BOX TOKEN'


def tweet_map():
    df = pd.read_sql(
        "SELECT * FROM got_sentiment ORDER BY unix DESC", conn)
    df.sort_values('unix', inplace=True)
    df.dropna(inplace=True)
    df_ll = df.copy()
    df_ll = df_ll.loc[(df_ll['lat'] != '') & (df_ll['long'] != '')]
    df_ll['lat'] = pd.to_numeric(df_ll.lat, errors='coerce')
    df_ll['long'] = pd.to_numeric(df_ll.long, errors='coerce')

    data = [
        go.Scattermapbox(
            lat=df_ll['lat'],
            lon=df_ll['long'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=17,
                color='rgb(255, 0, 0)',
                opacity=0.7
            )
        ),
        go.Scattermapbox(
            lat=df_ll['lat'],
            lon=df_ll['long'],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=7,
                color='rgb(242, 177, 172)',
                opacity=0.7
            ),
            hoverinfo='none'
        )]

    layout = go.Layout(
        title='Game of Thrones Tweet Map',
        autosize=True,
        hovermode='closest',
        showlegend=False,
        mapbox=go.layout.Mapbox(
            accesstoken=mapbox_access_token,
            bearing=0,
            center=go.layout.mapbox.Center(
                lat=38,
                lon=-94
            ),
            pitch=0,
            zoom=2,
            style='light'
        ),
    )

    return go.Figure(data=data, layout=layout)


app.layout = html.Div(className='container-fluid', children=[
    html.Div([
        html.H1(children="Game of Thrones Twitter Sentiment"),
        dcc.Dropdown(
            id='input-dropdown',
            options=[
                {'label': 'Overall', 'value': '#gameofthrones'},
                {'label': 'Jon Snow', 'value': 'jon'},
                {'label': 'Daenarys', 'value': 'daenarys'},
                {'label': 'Tyrion', 'value': 'tyrion'},
                {'label': 'Cersei', 'value': 'cersei'},
                {'label': 'Jaime', 'value': 'jaime'},
                {'label': 'Grey Worm', 'value': 'grey worm'},
                {'label': 'Arya', 'value': 'arya'},
                {'label': 'Clegane Bowl', 'value': 'clegane'},
                {'label': 'Qyburn', 'value': 'qyburn'},
                {'label': 'Euron', 'value': 'euron'},
            ],
            value='#gameofthrones',
        ),
    ]),
    html.Div(className='row', children=[
        html.Div([
            dcc.Graph(id='output-graph')]),
        html.Div([
            dcc.Graph(id='output-map', figure=tweet_map())
        ])
    ])
])


'''the sentiment graph needs a callback in order to update based on
    various queries.
'''


@app.callback(
    Output('output-graph', 'figure'),
    [Input('input-dropdown', 'value')]
)
def update_graph_scatter(value):
    try:
        df = pd.read_sql(
            "SELECT * FROM got_sentiment WHERE lang LIKE ? AND tweet LIKE ? ORDER BY unix DESC", conn, params=('%en%', '%' + value + '%',))
        df.sort_values('unix', inplace=True)
        df.dropna(inplace=True)
        df['date'] = pd.to_datetime(df['unix'], unit='ms')
        df.set_index('date', inplace=True)
        df['smoothed'] = df['sentiment'].rolling(int(len(df)/10)).mean()
        df = df.resample('1s').mean()
        X = df.index
        Y = df.smoothed.values
        return {
            'data': [go.Scatter(
                x=X,
                y=Y,
                name='Scatter',
                mode='lines+markers'
            )],
            'layout': go.Layout(
                xaxis=dict(range=[min(X), max(X)]),
                yaxis=dict(range=[min(Y), max(Y)]),
                title='Sentiment for: "{}"'.format(value)
            )
        }

    except Exception as e:
        with open('errors.txt', 'a') as f:
            f.write(str(e))
            f.write('\n')


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
