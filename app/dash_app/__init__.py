import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

air = pd.read_csv('http://data.insideairbnb.com/united-states/il/chicago/2021-04-19/visualisations/listings.csv')

fig = px.scatter_mapbox(air, lat="latitude", lon="longitude", hover_name="neighbourhood", hover_data=[
    "room_type", "price"], size="price", color="neighbourhood", zoom=11, height=400)

fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

def create_dash_application(flask_app):
    dash_app=dash.Dash(server=flask_app, name="dashboard", url_base_pathname="/dash/")

    dash_app.layout = html.Div(children=[
        
        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])

    return dash_app

if __name__ == '__main__':
    app.run_server(debug=True)
