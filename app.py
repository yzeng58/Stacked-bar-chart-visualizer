# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

import dash, os, base64, datetime, io
import dash_table as dt
import dash_core_components as dcc
import dash_html_components as html
from dash_daq import DarkThemeProvider
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

GRAPH_INTERVAL = os.environ.get("GRAPH_INTERVAL", 5000)
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
app.title = 'Stacked bar chart Dashboard'
server = app.server

axis_color = {"dark": "#EBF0F8", "light": "#506784"}
marker_color = {"dark": "#f2f5fa", "light": "#2a3f5f"}

theme = {
    "dark": False,
    "primary": "#447EFF",
    "secondary": "#D3D3D3",
    "detail": "#D3D3D3",
}

colors = {
    'background': "#FFFFFF", # '#111111',
    'text': "#000000" # '#7FDBFF'
}

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

df = pd.read_csv('Medals.csv')
df = df.sort_values('Total', ascending = False)

df2 = pd.DataFrame({
    'year': [1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003,
         2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012],
    'China': [16, 13, 10, 11, 28, 37, 43, 55, 56, 88, 105, 156, 270,
                   299, 340, 403, 549, 499],
    'Rest of world': [219, 146, 112, 127, 124, 180, 236, 207, 236, 263,
                   350, 430, 474, 526, 488, 537, 500, 439]
})

dfs = {'Medals': df, 'US export of plastic scrap': df2}

width_int = (200,1200,900)
height_int = (200, 1000, 800)
default_fig = px.bar(df, x="Team/NOC", y=['Gold', 'Silver', 'Bronze'], title="Resized figure", width = 500, height = 500)

default_fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

def parse_contents(contents, filename):
    _, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        assert(filename.split('.')[-1] == 'csv')
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        return html.Div([
            'Only .csv file is supported.'
        ])
    return df

def header():
    return [
                html.H2( # header
                    children='Stacked bar chart generator',
                ),
                html.Img(
                        src=app.get_asset_url("logo.png"),
                        className="logo",
                ),
                dcc.Location(id='url'),
            ]

def left_panel():
    return  [
                dcc.Graph(
                    id='graph',
                    figure=default_fig,
                ),
            ]

def right_panel():
    return [
                html.H6('Dataset'),
                html.Div([
                    dcc.Upload(
                        id = 'upload-data',
                        children = html.Div(['Drag and Drop or ', html.A('Select .csv Files')]),      
                        style = {
                            'width': '95%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                    ),
                ]), # , style={'width': '50%', 'display': 'inline-block'}),
                html.Div([
                    dcc.Dropdown(
                        id='data',
                        options=[{'label': i, 'value': i} for i in ['Medals', 'US export of plastic scrap']],
                        value='Medals'
                    ),
                ]),# , style={'width': '50%', 'display': 'inline-block'}),

                html.Div([
                    html.H6('Table Preview (first 10 rows)'),
                    dt.DataTable(
                        style_data={
                            'whiteSpace': 'normal',
                            'height': 'auto',
                            'lineHeight': '15px',
                        },
                        id='table', data=df[:10].to_dict('records'),
                        columns=[{"name": i, "id": i} for i in df.columns],
                    ),
                ]),

                html.Div([
                    html.H6('Settings'),
                ]), 
                
                html.Div([
                    html.Br(),
                    html.Label('Variable y'),
                    dcc.Dropdown(
                        id='y',
                        options=[
                            {'label': 'Gold', 'value': 'Gold'},
                            {'label': 'Silver', 'value': 'Silver'},
                            {'label': 'Bronze', 'value': 'Bronze'}
                        ],
                        value=['Gold', 'Silver', 'Bronze'],
                        multi=True
                    ),
                ], style={'width': '50%', 'display': 'inline-block'}),

                html.Div([
                    html.Label('Variable x'),
                    dcc.Dropdown(
                        id='x',
                        options=[{'label': i, 'value': i} for i in ['Team/NOC']],
                        value='Team/NOC'
                    ),
                ], style={'width': '50%', 'display': 'inline-block'}),

                # html.Div([
                #     html.Label('Variable y'),
                #     dcc.Dropdown(
                #         id='y',
                #         options=[{'label': i, 'value': i} for i in ['None']],
                #         value='None'
                #     ),
                # ], style={'width': '50%', 'display': 'inline-block'}),

                html.Br(), # line break
                html.Br(), # line break
                html.Div([
                    html.Label('Width'),
                    dcc.Slider(
                        id = 'width',
                        min=width_int[0],
                        max=width_int[1],
                        step = 25,
                        marks={i: str(i) for i in range(width_int[0], width_int[1]+100, 100)},
                        value=width_int[2],
                    ),
                ]),

                html.Div([
                    html.Label('Height'),
                    dcc.Slider(
                        id = 'height',
                        min=height_int[0],
                        max=height_int[1],
                        step = 25,
                        marks={i: str(i) for i in range(height_int[0], height_int[1]+100, 100)},
                        value=height_int[2],
                    ),
                ]),

                dcc.Markdown('''
                ------------------------------------------------------------------------------------------------------------------
                '''),
                dcc.Markdown('''
                    Developed by [Yuchen Zeng](https://yzeng58.github.io/zyc_cv/) and [Lihe Liu](http://liheliu95.me/about/).
                '''),
            ]

app.layout = html.Div(
    [
        # header
        html.Div(
            header(),
            className='banner row',
        ),
        # left panel
        html.Div(
            left_panel(),
            style={'width': '65%', 'display': 'inline-block'},
        ),
        # right panel
        html.Div(
            right_panel(),
            className="light-card",
            style={'width': '32%', 'display': 'inline-block'},
        )
    ]
)

# change dataset
@app.callback(
    [
        Output('table', 'data'), Output('table', 'columns'),
        Output('y', 'options'), Output('y', 'value'),
        Output('x', 'options'), Output('x', 'value')
    ],
    [
        Input('data', 'value'),
        Input('upload-data', 'contents'),
    ],
    State('upload-data', 'filename'),
)
def update_data(tab_name, content, filename):
    if tab_name == 'US export of plastic scrap':
        df = dfs[tab_name]
        return (
            df[:10].to_dict('records'),
            [{"name": i, "id": i} for i in df.columns],
            [
                {'label': 'China', 'value': 'China'},
                {'label': 'Rest of world', 'value': 'Rest of world'}
            ],
            ['China', 'Rest of world'],
            [{'label': 'year', 'value': 'year'}],
            'year'
        )
    elif tab_name == 'Medals':
        df = dfs[tab_name]
        return (
            df[:10].to_dict('records'),
            [{"name": i, "id": i} for i in df.columns],
            [  
                {'label': 'Gold', 'value': 'Gold'},
                {'label': 'Silver', 'value': 'Silver'},
                {'label': 'Bronze', 'value': 'Bronze'}
            ],
            ['Gold', 'Silver', 'Bronze'],
            [{'label': 'Team/NOC', 'value': 'Team/NOC'}],
            'Team/NOC'
        )
    else:
        df = parse_contents(content, filename)
        return (
            df[:10].to_dict('records'),
            [{"name": i, "id": i} for i in df.columns],
            [{'label': i, 'value': i} for i in df.columns],
            None,
            [{'label': i, 'value': i} for i in df.columns],
            None,
        )



# update figure
@app.callback(
    Output('graph', 'figure'),
    [
        Input('data', 'value'),
        Input('width', 'value'),
        Input('height', 'value'),
        Input('y', 'value'),
        Input('x', 'value'),
        Input('upload-data', 'contents')
    ],
    [
        State("graph", "figure"),
        State('upload-data', 'filename')
    ]
)
def update_figure(tab_name, width, height, y, x, content, fig_json, filename):
    fig = go.Figure(fig_json)
    if tab_name in ['US export of plastic scrap', 'Medals']:
        fig = px.bar(dfs[tab_name], x=x, y=y, title="Resized figure")
    else:
        df = parse_contents(content, filename)
        if x and y:
            fig = px.bar(df, x=x, y=y, title="Resized figure")
        else:
            fig = px.bar(title="Resized figure")

    fig.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'],
        width = int(width),
        height = int(height)
    )
    fig.update_layout(width = int(width), height = int(height))
    return fig

@app.callback(
    [
        Output('data', 'options'),
        Output('data', 'value')
    ],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        if isinstance(list_of_names, str):
            return ([{'label': i, 'value': i} for i in ['Medals', 'US export of plastic scrap', list_of_names]], list_of_names)
        elif isinstance(list_of_names, list):
            return ([{'label': i, 'value': i} for i in ['Medals', 'US export of plastic scrap'] + list_of_names], list_of_names[-1])
    else:
        return ([{'label': i, 'value': i} for i in ['Medals', 'US export of plastic scrap']], 'Medals')

# upload dataset
# @app.callback(
#     Output('graph', 'figure'),
#     [
#         Input('data', 'value'),
#     ],
# )
# def update_figure(tab_name, width, height, y, x, fig_json):
#     fig = go.Figure(fig_json)
#     fig = px.bar(dfs[tab_name], x=x, y=y, title="Resized figure")

#     fig.update_layout(
#         plot_bgcolor=colors['background'],
#         paper_bgcolor=colors['background'],
#         font_color=colors['text'],
#         width = int(width),
#         height = int(height)
#     )
#     fig.update_layout(width = int(width), height = int(height))
#     return fig



# get the screen size
# @app.clientside_callback(
#     """
#     function(href) {
#         var w = window.innerWidth;
#         var h = window.innerHeight;
#         return {'height': h, 'width': w};
#     }
#     """,
#     [
#         Output('height', 'value'),
#         Output('height', 'max'),
#         Output('height', 'marks'),
#         Output('width', 'value'),
#         Output('width', 'max'),
#         Output('width', 'marks'),
#     ],
#     Input('url', 'href')
# )
# def getSize(window):
#     w = window.innerWidth
#     h = window.innerHeight
#     print(w,h)
#     return (
#         height_int[1],
#         height_int[1],
#         {i: str(i) for i in range(height_int[0], height_int[1]+100, 100)},
#         width_int[1],
#         width_int[1],  
#         {i: str(i) for i in range(width_int[0], width_int[1]+100, 100)}
#     )


if __name__ == '__main__':
    app.run_server(debug=True, port = 1234)