# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                                    options=[
                                                         {'label': 'ALL SITES', 'value': 'ALL'},
                                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                    ],
                                            value='ALL',
                                            placeholder="place holder here", 
                                            searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload_range',min=0, max=10000, step=1000, 
                                                            marks={0: '0', 1000: '1000', 2000: '2000', 3000: '3000', 4000: '4000', 5000: '5000',
                                                                         6000: '6000', 7000: '7000', 8000: '8000', 9000: '9000', 10000: '10000'},
                                        value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='scatter_chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(data_frame = filtered_df, names='Launch Site', values='class' ,title='Total Success Launches by Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        specific_df = filtered_df.loc[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(data_frame = specific_df, names='class' ,title='Total Launches for Site '+ entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='scatter_chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),
              Input(component_id='payload_range', component_property='value')])
def get_scatter_plot(entered_site,payload_limits):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        specific_df = filtered_df[(filtered_df['Payload Mass (kg)']>=payload_limits[0])  
                        &(filtered_df['Payload Mass (kg)']<=payload_limits[1])]
        fig = px.scatter(data_frame = specific_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig
    else:
        df = filtered_df.loc[filtered_df['Launch Site'] == entered_site]
        specific_df = df[(df['Payload Mass (kg)']>=payload_limits[0])  
                        &(df['Payload Mass (kg)']<=payload_limits[1])]
        fig = px.scatter(data_frame = specific_df, x="Payload Mass (kg)", y="class", color="Booster Version Category")
        return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
