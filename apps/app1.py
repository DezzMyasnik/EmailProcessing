# -*- coding: utf-8 -*-

# Загрузим необходимые пакеты
import dash
import dash_core_components as dcc
import dash_html_components as html
import init_db
import pandas as pd
from dash.dependencies import Output, Input
import plotly
from app import app
import plotly.express as px
#  Объяснение данных строк пока опускается, будет объяснено далее

external_stylesheets = ['style.css']

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

with init_db.db_session:
    x = init_db.select([p.name_of_class, p.count_of_emails] for p in init_db.Class_of_mail)[:]
#y  = init_db.Class_of_mail.count_of_emails

"""
html.Ul(children=[html.Li(children=[dcc.Link('На главную', href='/')]),
                      html.Li(children=[dcc.Link('К статистике', href='/apps/app1')]),
                      html.Li(children=[dcc.Link('К обучающей выборке', href='/apps/app2')]),
                      html.Li(children=[dcc.Link('К водопаду писем', href='/apps/app3')])
                      ]),
"""
layout = html.Div(children=[
    html.Div(id='app-1-display-value'),

    html.H1(children='Сервер сортировки почты'),
    html.Div(children='''
        Критерии классификации и количество выявленных писем
    '''),
    dcc.Graph(
        id='live-update-graph-bar',
        animate=True,
    ),
    dcc.Graph(
        id='live-update-graph-some',
        animate=True,
    ),
    dcc.Textarea(
        id='textarea-example_1',
        #value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '100%', 'height': 200},
    ),

    dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        ),
])
"""
dcc.Graph(
        id='live-update-graph-per-hour',
        animate=True, ),
figure={
            'data': [
                {'x': [xx[0] for xx in x], 'y': [yy[1] for yy in x],
                 'type': 'bar',
                 'text':  [yy[1] for yy in x],
                 'textposition': 'outside',
                 'name': 'Критерии классификации'},

            ],
            'layout': {
                'title': 'Классификаторы'
            }
        }"""
@app.callback(
    Output('app-1-display-value', 'children'),
    Input('app-1-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)

@app.callback(Output('live-update-graph-bar', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_bar(n):

    #traces = list()
    with init_db.db_session:
        x = init_db.select([p.name_of_class, p.count_of_emails] for p in init_db.Class_of_mail)[:]

    #tr = [plotly.graph_objs.Pie(values=[xx[0] for xx in x],text=[yy[1] for yy in x])]
    traces=[plotly.graph_objs.Bar(
            x=[xx[0] for xx in x],
            y=[yy[1] for yy in x],
            textposition = 'outside',
            text=  [yy[1] for yy in x],
            name ='Критерии классификации',


            )]

    #traces =[]
    layout = plotly.graph_objs.Layout(title='Классификаторы')
    fig = {'data': traces, 'layout': layout}
    return fig

@app.callback(Output('live-update-graph-some', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_some(n):

    #traces = list()
    with init_db.db_session:
        df = pd.read_sql('select * from Class_of_mail', init_db.db.get_connection())

    #fig = px.pie(df,values="count_of_emails",names='name_of_class',title='name_of_class')
    fig = px.histogram(df,y ='count_of_emails', x='name_of_class', color='name_of_class',log_y=True, )
                     #y="name_of_class",
                    ## size="count_of_emails",
                    #    hover_name="name_of_class", log_x=True, )
    #tr = [plotly.graph_objs.Pie(values=[xx[0] for xx in x],text=[yy[1] for yy in x])]
    #traces=[plotly.graph_objs.Candlestick(x=[xx[0] for xx in x], text=[yy[1] for yy in x])

        #]
    """
    Bar(
        x=[xx[0] for xx in x],
        y=[yy[1] for yy in x],
        textposition='outside',
        text=[yy[1] for yy in x],
        name='Критерии классификации'

    )
    """
    #traces =[]
    layout = plotly.graph_objs.Layout(title='Классификаторы')
    #fig = {'data': traces, 'layout': layout}
    return fig

@app.callback(
    Output('textarea-example_1', 'value'),
    Input('interval-component', 'n_intervals'),

)
def update_output(n_intervals):
    with open('sort.log','r', encoding='utf-8') as file:
        lines = file.readlines()
        #lines = lines.reverse()
    lines = list(reversed(lines))

    lines = '\n'.join(lines[:10])
    return lines
