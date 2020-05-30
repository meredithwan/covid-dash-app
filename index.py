import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc

from app import server
from app import app
from apps import global_situation, singapore, home

# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Global", href="/global_situation")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("More pages", header=True),
#                 dbc.DropdownMenuItem("Singapore", href="/singapore"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="More",
#         ),
#     ],
#     brand="NavbarSimple",
#     brand_href="#",
#     color="primary",
#     dark=True,
# )

dropdown = dbc.DropdownMenu(
    children=[
        #dbc.DropdownMenuItem("Explore", header=True),
        dbc.DropdownMenuItem("Home", href="/haha"),
        dbc.DropdownMenuItem("Global", href="/global_situation"),
        dbc.DropdownMenuItem("Singapore", href="/singapore"),
    ],
    nav = True,
    in_navbar = True,
    label = "Explore",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src="/assets/virus.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("COVID-19 DASH", className="ml-2")),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                href="/home",
            ),
            dbc.NavbarToggler(id="navbar-toggler2"),
            dbc.Collapse(
                dbc.Nav(
                    [dropdown], className="ml-auto", navbar=True
                ),
                id="navbar-collapse2",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="mb-4",
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


# the same function (toggle_navbar_collapse) is used in all three callbacks
for i in [2]:
    app.callback(
        Output(f"navbar-collapse{i}", "is_open"),
        [Input(f"navbar-toggler{i}", "n_clicks")],
        [State(f"navbar-collapse{i}", "is_open")],
    )(toggle_navbar_collapse)

# navbar = dbc.Navbar(
#     dbc.Container(
#         [
#
#         ]
#     )
#     [
#     html.Div([
#         dbc.Row([
#             dbc.Col(html.Img(src="/assets/virus.png", height="30px")),
#                     dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
#                 ],
#                 align="center",
#                 no_gutters=True,
#             )
#         ]),
#     # dbc.NavItem(dbc.NavLink("Global", href="/global_situation")),
#     dbc.DropdownMenu(
#         children=[
#             dbc.DropdownMenuItem("Explore", header=True),
#             dbc.DropdownMenuItem("Global", href="/global_situation"),
#             dbc.DropdownMenuItem("Singapore", href="/singapore"),
#         ])
#     ],
#     color="primary",
#     dark=True,
# )

# navbar = dbc.Navbar(
#     [
#         html.A(
#             # Use row and col to control vertical alignment of logo / brand
#             dbc.Row(
#                 [
#                     dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
#                     dbc.Col(dbc.NavbarBrand("Navbar", className="ml-2")),
#                 ],
#                 align="center",
#                 no_gutters=True,
#             ),
#             href="https://plot.ly",
#         ),
#         dbc.NavbarToggler(id="navbar-toggler"),
#         dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
#     ],
#     color="dark",
#     dark=True,
# )



app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# index_page = html.Div([
#     html.H1(children="haha"),
# ])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    # if pathname == '/':
    #     return html.Div([
    #         dcc.Link('Global', href='/global_situation'),
    #         html.Br(),
    #         dcc.Link('Singapore', href='/singapore')
    #     ])

    if pathname == '/global_situation':
        return global_situation.layout
    elif pathname == '/singapore':
        return singapore.layout
    else:
        return home.layout

# @app.server.route('/static/<path>')
# def static_file(path):
#     static_folder = os.path.join(os.getcwd(), 'assets')
#     return send_from_directory(static_folder, path)

if __name__ == '__main__':
    app.run_server(debug=True)