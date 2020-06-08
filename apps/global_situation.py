import plotly.graph_objects as go
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from app import app

# needed if running single page dash app instead
#external_stylesheets = [dbc.themes.LUX]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('COVID-19-geographic-disbtribution-worldwide.csv', index_col = 0)

# preparing various dataframes for visualisation
from datetime import datetime
df.index = pd.to_datetime(df.index, format='%d/%m/%y')
df = df.sort_index()
# convert number of cases and deaths to per 1 million population figures
# to allow for comparison
df['cases per 1 mil'] = df['cases']/df['popData2018']*1000000
df['deaths per 1 mil'] = df['deaths']/df['popData2018']*1000000
# exclude observations from the Japan cruise ship
df = df[df.continentExp != 'Other']

df2 = df.copy()
df2 = df2.groupby(['continentExp','date']).sum()

df2 = df2.sort_values(['date'], ascending = True)
df3 = df2.copy()
df3 = df3.tail(5)
df3 = df3.reset_index()

df4 = df.copy()
df4 = df4.groupby(['continentExp']).sum()

# cumulative cases and deaths
df5 = df.copy()
df5 = df5.groupby(['continentExp','date']).sum()
df5 = df5.reset_index()
df5['cases per 1 mil'] = df5.groupby(['continentExp'])['cases per 1 mil'].apply(lambda x: x.cumsum())
df5['deaths per 1 mil'] = df5.groupby(['continentExp'])['deaths per 1 mil'].apply(lambda x: x.cumsum())

# good if there are many options
available_countries = df['countriesAndTerritories'].unique()

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='COVID-19 Worldwide at a glance'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising trends across the world'), className="mb-4")
        ]),
# choose between cases or deaths
    dcc.Dropdown(
        id='cases_or_deaths',
        options=[
            {'label': 'Cases per 1 million people', 'value': 'cases per 1 mil'},
            {'label': 'Deaths per 1 million people', 'value': 'deaths per 1 mil'},
        ],
        value='cases per 1 mil',
        #multi=True,
        style={'width': '50%'}
        ),
# for some reason, font colour remains black if using the color option
    dbc.Row([
        dbc.Col(dbc.Card(html.H3(children='Daily figures by continent (per 1 million people)',
                                 className="text-center text-light bg-dark"), body=True, color="dark")
        , className="mt-4 mb-4")
    ]),
    dbc.Row([
        dbc.Col(html.H5(children='Latest update: 7 June 2020', className="text-center"),
                         width=4, className="mt-4"),
        dbc.Col(html.H5(children='Daily figures since 31 Dec 2019', className="text-center"), width=8, className="mt-4"),
        ]),


    dbc.Row([
        dbc.Col(dcc.Graph(id='pie_cases_or_deaths'), width=4),
        dbc.Col(dcc.Graph(id='line_cases_or_deaths'), width=8)
        ]),

        dbc.Row([
            dbc.Col(dbc.Card(html.H3(children='Cumulative figures by continent (per 1 million people)',
                                     className="text-center text-light bg-dark"), body=True, color="dark")
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Latest update: 7 June 2020', className="text-center"),
                    width=4, className="mt-4"),
            dbc.Col(html.H5(children='Cumulative figures since 31 Dec 2019', className="text-center"), width=8,
                    className="mt-4"),
        ]),

    dbc.Row([
        dbc.Col(dcc.Graph(id='total_pie_cases_or_deaths'), width=4),
        dbc.Col(dcc.Graph(id='total_line_cases_or_deaths'), width=8)
    ]),

    dbc.Row([
        dbc.Col(dbc.Card(html.H3(children='Figures by country (per 1 million people)',
                                 className="text-center text-light bg-dark"), body=True, color="dark")
        , className="mb-4")
        ]),

    dcc.Dropdown(
        id='countries',
        options=[{'label': i, 'value': i} for i in available_countries],
        value=['Sweden', 'Switzerland'],
        multi=True,
        style={'width': '70%', 'margin-left': '5px'}
    ),

    dbc.Row([
        dbc.Col(html.H5(children='Daily figures', className="text-center"),
                className="mt-4"),
    ]),

    dcc.Graph(id='cases_or_deaths_country'),

    dbc.Row([
        dbc.Col(html.H5(children='Cumulative figures', className="text-center"),
                className="mt-4"),
    ]),

    dcc.Graph(id='total_cases_or_deaths_country'),

])


])

# page callbacks
# display pie charts and line charts to show number of cases or deaths
@app.callback([Output('pie_cases_or_deaths', 'figure'),
               Output('line_cases_or_deaths', 'figure'),
               Output('total_pie_cases_or_deaths', 'figure'),
               Output('total_line_cases_or_deaths', 'figure')],
              [Input('cases_or_deaths', 'value')])

def update_graph(choice):

    fig = go.Figure(data=[
        go.Pie(labels=df3['continentExp'], values=df3[choice])
        ])

    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      template = "seaborn",
                      margin=dict(t=0))

    dff = df2.copy()
    dff = pd.pivot_table(dff, values=choice, index=['date'], columns='continentExp')

    fig2 = go.Figure()
    for col in dff.columns:
        fig2.add_trace(go.Scatter(x=dff.index, y=dff[col].values,
                                 name=col,
                                 mode='markers+lines'))

    fig2.update_layout(yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    fig3 = go.Figure(data=[
        go.Pie(labels=df4.index, values=df4[choice])
        ])

    fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    dff2 = df5.copy()
    dff2 = pd.pivot_table(dff2, values=choice, index=['date'], columns='continentExp')

    fig4 = go.Figure()
    for col in dff2.columns:
        fig4.add_trace(go.Scatter(x=dff2.index, y=dff2[col].values,
                                 name=col,
                                 mode='markers+lines'))

    fig4.update_layout(yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    return fig, fig2, fig3, fig4

# to allow comparison of cases or deaths among countries
@app.callback([Output('cases_or_deaths_country', 'figure'),
               Output('total_cases_or_deaths_country', 'figure')],
              [Input('cases_or_deaths', 'value'),
               Input('countries', 'value')])

def update_graph(cases_or_deaths_name, countries_name):

    dfc = df.copy()
    dfc = dfc[dfc.countriesAndTerritories.isin(countries_name)]

    dfc = pd.pivot_table(dfc, values=cases_or_deaths_name, index=['date'], columns='countriesAndTerritories')

    dfc2 = df.copy()
    dfc2 = dfc2[dfc2.countriesAndTerritories.isin(countries_name)]

    dfc2 = dfc2.groupby(['countriesAndTerritories', 'date']).sum()
    dfc2 = dfc2.reset_index()
    dfc2['cases per 1 mil'] = dfc2.groupby(['countriesAndTerritories'])['cases per 1 mil'].apply(lambda x: x.cumsum())
    dfc2['deaths per 1 mil'] = dfc2.groupby(['countriesAndTerritories'])['deaths per 1 mil'].apply(lambda x: x.cumsum())

    dfc2 = pd.pivot_table(dfc2, values=cases_or_deaths_name, index=['date'], columns='countriesAndTerritories')

    fig5 = go.Figure()
    for col in dfc.columns:
        fig5.add_trace(go.Scatter(x=dfc.index, y=dfc[col].values,
                              name=col,
                              mode='markers+lines'))

    fig5.update_layout(yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    fig6 = go.Figure()
    for col in dfc2.columns:
        fig6.add_trace(go.Scatter(x=dfc2.index, y=dfc2[col].values,
                                  name=col,
                                  mode='markers+lines'))

        fig6.update_layout(yaxis_title='Number Per 1 Million',
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           template = "seaborn",
                           margin=dict(t=0))

    return fig5, fig6

# needed only if running this as a single page app
# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)