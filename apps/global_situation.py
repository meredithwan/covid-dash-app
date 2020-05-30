import plotly.graph_objects as go
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc

from app import app

#external_stylesheets = [dbc.themes.LUX]

#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('COVID-19-geographic-disbtribution-worldwide.csv', index_col = 0)

from datetime import datetime
df.index = pd.to_datetime(df.index, format='%d/%m/%y')
df = df.sort_index()
df['cases per 1 mil'] = df['cases']/df['popData2018']*1000000
df['deaths per 1 mil'] = df['deaths']/df['popData2018']*1000000
df = df[df.continentExp != 'Other']

df2 = df.copy()
df2 = df2.groupby(['continentExp','date']).sum()

df2 = df2.sort_values(['date'], ascending = True)
df3 = df2.copy()
df3 = df3.tail(5)
df3 = df3.reset_index()

df4 = df.copy()
df4 = df4.groupby(['continentExp']).sum()

df5 = df.copy()
df5 = df5.groupby(['continentExp','date']).sum()
df5 = df5.reset_index()
df5['cases per 1 mil'] = df5.groupby(['continentExp'])['cases per 1 mil'].apply(lambda x: x.cumsum())
df5['deaths per 1 mil'] = df5.groupby(['continentExp'])['deaths per 1 mil'].apply(lambda x: x.cumsum())

# good if there are many options
available_countries = df['countriesAndTerritories'].unique()

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1(children='COVID-19 Worldwide at a glance'), className="mb-2")
        ]),
        dbc.Row([
            dbc.Col(html.H6(children='Visualising trends across the world'), className="mb-4")
        ]),

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
                         #outline=True)
        , className="mt-4 mb-4")
    ]),
    dbc.Row([
        dbc.Col(html.H5(children='Latest update: 26 May 2020', className="text-center"),
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
                    # outline=True)
                    , className="mb-4")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='Latest update: 26 May 2020', className="text-center"),
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
                    # outline=True)
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

    #html.Div(
    #     dcc.RangeSlider(
    #     id='period_slider',
    #     min=12,
    #     max=5,
    #     value=[12,5],
    #     marks={12:"December 2019",
    #            1: "January 2020",
    #            2: "February 2020",
    #            3: "March 2020",
    #            4: "April 2020",
    #            5: "May 2020"},
    #     step=1
    # ), style={'width': '90%', 'padding': '0px 20px 20px 20px'})
])


])

# @app.callback([Output('datatable', 'data'),
#               Output('datatable', 'columns')],
#              [Input('table_type', 'value')])
#
# def update_columns(value):
#     df2 = df.tail(1)
#     col = ['Daily Imported', 'Daily Local transmission']
#     df2['Daily Confirmed Cases'] = df2[col].sum(axis=1)
#
#     condensed_col = ['Date', 'Daily Confirmed Cases', 'Cumulative Confirmed', 'Daily Discharged',
#                      'Cumulative Discharged', 'Daily Deaths', 'Cumulative Deaths', 'Daily Imported',
#                      'Local cases residing in dorms',
#                      'Local cases not residing in dorms']
#
#     full_col = ['Date', 'Daily Confirmed Cases', 'Cumulative Confirmed', 'Daily Discharged',
#                 'Cumulative Discharged', 'Daily Deaths', 'Cumulative Deaths', 'Daily Imported',
#                 'Local cases residing in dorms', 'Local cases not residing in dorms',
#                 'Intensive Care Unit', 'General wards', 'In Isolation']
#
#     if value == 'Condensed table':
#         columns = [{"name": i, "id": i} for i in condensed_col]
#         data=df2.to_dict('records')
#     elif value == 'Full table':
#         columns = [{"name": i, "id": i} for i in full_col]
#         data=df2.to_dict('records')
#     return data, columns

# @app.callback(Output('cases_pie_choice', 'figure'),
#               [Input('choice', 'value')])
#
# def update_graph(choice_name):
#     if choice_name == 'Daily':
#         fig2 = go.Figure()
#         fig2.add_trace(go.Pie(labels=df3['continentExp'], values=df3['cases per 1000 pop']))
#         # data = [go.Pie(labels=df3['continentExp'], values=df3['cases per 1000 pop'])]
#         #                #, name='Daily confirmed', marker_color='#525564')]
#         # layout = go.Layout(
#         #     title=go.layout.Title(text="Daily COVID-19 Cases in Singapore"),
#         #     # xaxis={'title': "Date"},
#         #     # yaxis={'title': "Cases"},
#         #     paper_bgcolor='rgba(0,0,0,0)',
#         #     plot_bgcolor='rgba(0,0,0,0)'
#         # )
#     else:
#         fig2 = go.Figure()
#         fig2.add_trace(go.Pie(labels=df4.index, values=df4['cases per 1000 pop']))
#
#     return fig2
        # data = [go.Pie(labels=df4.index, values=df4['cases per 1000 pop'])]
        # # , name='Daily confirmed', marker_color='#525564')]
        # layout = go.Layout(
        #     title=go.layout.Title(text="Daily COVID-19 Cases in Singapore"),
        #     # xaxis={'title': "Date"},
        #     # yaxis={'title': "Cases"},
        #     paper_bgcolor='rgba(0,0,0,0)',
        #     plot_bgcolor='rgba(0,0,0,0)'
        # )

    # data = [go.Scatter(x=dff['Date'], y=dff['total'],
    #                    mode='lines+markers',name='Daily confirmed', marker_color='#525564')]
    # layout = go.Layout(
    #     title=go.layout.Title(text="Daily COVID-19 Cases in Singapore"),
    #     #xaxis={'title': "Date"},
    #     yaxis={'title': "Cases"},
    #     paper_bgcolor = 'rgba(0,0,0,0)',
    #     plot_bgcolor = 'rgba(0,0,0,0)'
    # )

    # fig = go.Figure()
    # fig.add_trace(go.Scatter(x=dff['Date'], y=dff['total'],
    #                                       mode='lines+markers',name='Daily confirmed cases'))
    #
    # # edit layout
    # fig.update_layout(title='Transmissions in Singapore',
    #                    xaxis_title='Date',
    #                    yaxis_title='Number of cases',
    #                   plot_bgcolor='rgba(0,0,0,0)')
    # return figure

    #return {'data': data, 'layout': layout}

# @app.callback([Output('local and imported', 'figure'),
#                Output('dorms', 'figure')],
#     [Input('graph_by_period', 'hoverData')])
#      #Input('covid_period', 'value')])
#
# def update_breakdown(hoverData):
#     day = hoverData['points'][0]['x']
#     dff = df[df['Date'] == day]
#     #dff = dff[dff.Period == covid_period_name]
#     fig2 = go.Figure()
#     fig2.add_trace(go.Bar(x=dff['Date'], y=dff['Daily Local transmission'],
#                           marker_color='#74828F', name='Local cases'))
#     fig2.add_trace(go.Bar(x=dff['Date'], y=dff['Daily Imported'],
#                           marker_color='#96C0CE', name='Imported cases'))
#
#     # edit layout
#     fig2.update_layout(title='Breakdown of cases: Local vs imported',
#                     #xaxis_title='Date',
#                     yaxis_title='Cases',
#                     paper_bgcolor='rgba(0,0,0,0)',
#                     plot_bgcolor='rgba(0,0,0,0)')
#
#     fig3 = go.Figure()
#     fig3.add_trace(go.Bar(x=dff['Date'], y=dff['Local cases residing in dorms'],
#                           marker_color='#BEB9B5', name='Residing in dorms'))
#     fig3.add_trace(go.Bar(x=dff['Date'], y=dff['Local cases not residing in dorms'],
#                           marker_color='#C25B56', name='Not residing in dorms'))
#
#     # edit layout
#     fig3.update_layout(title='Breakdown of cases: Whether residing in dorms',
#                        #xaxis_title='Date',
#                        yaxis_title='Cases',
#                        paper_bgcolor='rgba(0,0,0,0)',
#                        plot_bgcolor='rgba(0,0,0,0)')
#     return fig2, fig3
#
@app.callback([Output('pie_cases_or_deaths', 'figure'),
               Output('line_cases_or_deaths', 'figure'),
               Output('total_pie_cases_or_deaths', 'figure'),
               Output('total_line_cases_or_deaths', 'figure')],
              [Input('cases_or_deaths', 'value')])

def update_graph(choice):

    fig = go.Figure(data=[
        go.Pie(labels=df3['continentExp'], values=df3[choice])
        ])

    fig.update_layout(#title='Latest Daily Figure by Continent (26 May 2020)',
                      paper_bgcolor='rgba(0,0,0,0)',
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

    fig2.update_layout(#title='Daily Figures by Continent',
                       yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    fig3 = go.Figure(data=[
        go.Pie(labels=df4.index, values=df4[choice])
        ])

    fig3.update_layout(#title='Latest Total Figure by Continent (26 May 2020)',
                       paper_bgcolor='rgba(0,0,0,0)',
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

    fig4.update_layout(#title='Daily Figures by Continent',
                       yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    return fig, fig2, fig3, fig4

@app.callback([Output('cases_or_deaths_country', 'figure'),
               Output('total_cases_or_deaths_country', 'figure')],
              [Input('cases_or_deaths', 'value'),
               Input('countries', 'value')])#,
               #Input('period_slider', 'value')])

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

    fig5.update_layout(#title='Daily Figures by Country',
                       yaxis_title='Number Per 1 Million',
                       paper_bgcolor='rgba(0,0,0,0)',
                       plot_bgcolor='rgba(0,0,0,0)',
                       template = "seaborn",
                       margin=dict(t=0))

    fig6 = go.Figure()
    for col in dfc2.columns:
        fig6.add_trace(go.Scatter(x=dfc2.index, y=dfc2[col].values,
                                  name=col,
                                  mode='markers+lines'))

        fig6.update_layout(#title='Cumulative Figures by Country',
                           yaxis_title='Number Per 1 Million',
                           paper_bgcolor='rgba(0,0,0,0)',
                           plot_bgcolor='rgba(0,0,0,0)',
                           template = "seaborn",
                           margin=dict(t=0))

    return fig5, fig6


# if __name__ == '__main__':
#     app.run_server(host='127.0.0.1', debug=True)