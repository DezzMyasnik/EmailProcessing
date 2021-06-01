# -*- coding: utf-8 -*-

# Загрузим необходимые пакеты
import dash
import dash_core_components as dcc
import dash_html_components as html
import init_db
from dash.dependencies import Output, Input
import plotly
#  Объяснение данных строк пока опускается, будет объяснено далее

external_stylesheets = ['style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

with init_db.db_session:
    x =  init_db.select([p.name_of_class, p.count_of_emails] for p in init_db.Class_of_mail)[:]
#y  = init_db.Class_of_mail.count_of_emails


app.layout = html.Div(children=[
    html.H1(children='Сервер сортиовки почты'),

    html.Div(children='''
        Критерии классификации и количество выявленных писем
    '''),

    dcc.Graph(
        id='live-update-graph-bar',
        animate=True,

    ),
    dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )
])
"""
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


@app.callback(Output('live-update-graph-bar', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_bar(n):

    #traces = list()
    with init_db.db_session:
        x = init_db.select([p.name_of_class, p.count_of_emails] for p in init_db.Class_of_mail)[:]


    traces=[plotly.graph_objs.Bar(
            x=[xx[0] for xx in x],
            y=[yy[1] for yy in x],
            textposition = 'outside',
            text=  [yy[1] for yy in x],
            name ='Критерии классификации'

            )]

    #traces =[]
    layout = plotly.graph_objs.Layout(title='Классификаторы')
    fig = {'data': traces, 'layout': layout}
    return fig



if __name__ == '__main__':
    app.run_server(debug=True)