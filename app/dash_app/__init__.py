import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# Chicago
air = pd.read_csv(
    'http://data.insideairbnb.com/united-states/il/chicago/2021-04-19/visualisations/listings.csv')

fig = px.scatter_mapbox(air, lat="latitude", lon="longitude", hover_name="neighbourhood", hover_data=[
    "room_type", "price"], size="price", color="neighbourhood", zoom=11, height=400)

fig.update_layout(mapbox_style="carto-darkmatter")
fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

def create_dash_application(flask_app):
    dash_app = dash.Dash(server=flask_app, name="dashboard", url_base_pathname="/chicago-map/")

    dash_app.layout = html.Div(children=[

        dcc.Graph(
            id='example-graph',
            figure=fig
        )
    ])
    return dash_app


# Austin
aust = pd.read_csv(
    'http://data.insideairbnb.com/united-states/co/denver/2021-03-29/visualisations/listings.csv')

ausfig = px.scatter_mapbox(aust, lat="latitude", lon="longitude", hover_name="neighbourhood", hover_data=[
    "room_type", "price"], size="price", color="neighbourhood", zoom=11, height=400)

ausfig.update_layout(mapbox_style="carto-darkmatter")
ausfig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

def create_denver_application(flask_app):
    dash_app2 = dash.Dash(server=flask_app, url_base_pathname="/austin-map/")

    dash_app2.layout = html.Div(children=[

        dcc.Graph(
            id='example-graph',
            figure=ausfig
        )
    ])
    return dash_app2


# Boston
bos = pd.read_csv(
    'http://data.insideairbnb.com/united-states/ma/boston/2021-04-20/visualisations/listings.csv')

bosfig = px.scatter_mapbox(bos, lat="latitude", lon="longitude", hover_name="neighbourhood", hover_data=[
    "room_type", "price"], size="price", color="neighbourhood", zoom=11, height=400)

bosfig.update_layout(mapbox_style="carto-darkmatter")
bosfig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


def create_boston_application(flask_app):
    dash_app3 = dash.Dash(server=flask_app, url_base_pathname="/boston-map/")

    dash_app3.layout = html.Div(children=[

        dcc.Graph(
            id='example-graph',
            figure=bosfig
        )
    ])
    return dash_app3



# Dallas
dal = pd.read_csv(
    'http://data.insideairbnb.com/united-states/ca/los-angeles/2021-04-07/visualisations/listings.csv')

dalfig = px.scatter_mapbox(dal, lat="latitude", lon="longitude", hover_name="neighbourhood", hover_data=[
    "room_type", "price"], size="price", color="neighbourhood", zoom=9, height=400)

dalfig.update_layout(mapbox_style="carto-darkmatter")
dalfig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


def create_la_application(flask_app):
    dash_app4 = dash.Dash(server=flask_app, url_base_pathname="/dallas-map/")

    dash_app4.layout = html.Div(children=[

        dcc.Graph(
            id='example-graph',
            figure=dalfig
        )
    ])
    return dash_app4


# SF
sf = pd.read_csv(
    'http://data.insideairbnb.com/united-states/ca/san-francisco/2021-04-07/visualisations/listings.csv')

sffig = px.scatter_mapbox(sf, lat="latitude", lon="longitude", hover_name="neighbourhood", hover_data=[
    "room_type", "price"], size="price", color="neighbourhood", zoom=11, height=400)

sffig.update_layout(mapbox_style="carto-darkmatter")
sffig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})


def create_sf_application(flask_app):
    dash_app4 = dash.Dash(server=flask_app, url_base_pathname="/sf-map/")

    dash_app4.layout = html.Div(children=[

        dcc.Graph(
            id='example-graph',
            figure=sffig
        )
    ])
    return dash_app4









if __name__ == '__main__':
    app.run_server(debug=True)
