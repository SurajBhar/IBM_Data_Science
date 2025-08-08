import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the SpaceX data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1(
        'SpaceX Launch Records Dashboard',
        style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}
    ),

    # TASK 1: Dropdown for Launch Site selection
    dcc.Dropdown(
        id='site-dropdown',
        options=[
            {'label': 'All Sites', 'value': 'ALL'},
        ] + [{'label': site, 'value': site} for site in spacex_df['Launch Site'].unique()],
        value='ALL',
        placeholder='Select a Launch Site',
        searchable=True
    ),
    html.Br(),

    # TASK 2: Pie chart
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),

    html.P("Payload range (Kg):"),

    # TASK 3: RangeSlider for payload mass
    dcc.RangeSlider(
        id='payload-slider',
        min=min_payload,
        max=max_payload,
        step=1000,
        marks={i: str(i) for i in range(int(min_payload), int(max_payload) + 1, 1000)},
        value=[min_payload, max_payload]
    ),
    html.Br(),

    # TASK 4: Scatter chart
    html.Div(dcc.Graph(id='success-payload-scatter-chart')),
])

# TASK 2 Callback: update pie chart based on selected site
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        df = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig = px.pie(
            df,
            names='Launch Site',
            values='class',
            title='Total Successful Launches by Site'
        )
    else:
        df = spacex_df[spacex_df['Launch Site'] == selected_site]
        counts = df['class'].value_counts().sort_index().reset_index()
        counts.columns = ['class', 'count']
        # Map 0/1 to meaningful labels and fix colors
        counts['class'] = counts['class'].map({0: 'Failure', 1: 'Success'})
        fig = px.pie(
            counts,
            names='class',
            values='count',
            title=f'Success vs. Failure for site {selected_site}',
            color='class',
            color_discrete_map={'Failure': 'red', 'Success': 'green'}
        )
    return fig

# TASK 4 Callback: update scatter based on site and payload range
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    [
        Input('site-dropdown', 'value'),
        Input('payload-slider', 'value')
    ]
)
def update_scatter_chart(selected_site, payload_range):
    low, high = payload_range
    mask = (
        (spacex_df['Payload Mass (kg)'] >= low) &
        (spacex_df['Payload Mass (kg)'] <= high)
    )
    filtered_df = spacex_df[mask]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    # Roll back to original style: color by Booster Version Category, class on y-axis
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Success for all sites'
    )
    return fig

# Run the app using the default command
if __name__ == '__main__':
    app.run()
