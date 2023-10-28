# Import packages
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc


# Initialize venues dataset 
venues = pd.read_csv('../wedding_venue_dash-main/la_wedding_venue_data_lat_long.csv')
venues_table = venues.drop(columns=['region', 'country', 'postal code', 'latitude', 'longitude'])
#initialize app using Dash framework
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

'''
Build out html layout using a Div for the title, dropdown option to select sectors for presentation, table to show details,
a row in bootstrap to contain the histogram graph and scatter map plot of locations in LA
'''
app.layout = html.Div( style={'text-align':'center'},
    className= 'ricky-site',
    children=[
        html.Div(
            children=[
            html.H1('Wedding Venue Price Dashboard', className='wed-title'),
            dbc.Col(dcc.Dropdown(className='ricky-site',id='controls', 
                                 options=[{'label': i, 'value': i} for i in venues['sector'].unique()],
                                 value='Banquet Halls',
                                 style={'margin':'auto', 'width':'90%'}))
        ]),
        
        dbc.Row([
            dbc.Col(dash_table.DataTable(id='table',page_size=10, fill_width=True,
                             style_cell={'text-align':'left'}, 
                             style_header={'backgroundColor': '#222831', 'color':'#EEEEEE', 
                                           'text-transform':'uppercase', 'font-weight':'bold'},
                             style_data={'backgroundColor': '#222831', 'color':'#EEEEEE'}), 
                             style = {'padding':'1rem'},
                             lg=6),
            dbc.Col([html.Div([dcc.Graph(figure={}, id='graph')])], style ={'padding': '1rem'},
                    lg=6)
            ]),
         dbc.Row([
            dbc.Col(dcc.Graph(figure={}, id='map'), style={'padding':'.5 rem'}, lg=12)
            ])

    ])

#build callback features to control input values via dropdown, and output to the table, graph, and map
@app.callback(
    [Output(component_id='graph', component_property='figure'),
    Output(component_id='table', component_property='data'),
    Output(component_id='map', component_property='figure')],
    Input(component_id='controls', component_property='value')
)

#run function upon callback to update the table, graph, and map 
def update_hist_and_table(sector):
    hist = px.histogram(venues[venues['sector'] == sector], x='price', labels={'price': 'Venue Price'})
    table = venues_table[venues_table['sector'] == sector].to_dict('records')
    fig = px.scatter_mapbox(venues[venues['sector']==sector], lat='latitude', lon='longitude', hover_name='vendor name', 
                            hover_data = ['price'])
    fig.update_layout(mapbox_style="stamen-toner")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    fig.update_traces(marker=dict(size=15))
    return hist, table, fig

#run application
if __name__ == '__main__':
    app.run_server(debug=True)
