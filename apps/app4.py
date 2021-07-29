# -*- coding: utf-8 -*-

# Загрузим необходимые пакеты
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import dash_daq as daq
from app import app
from subprocess import Popen
import sys
import settings

P = None

def thread_second():
    #d = sys.executable
    return Popen([sys.executable, "Bot.py"])
    #return Popen([sys.executable, ".\Bot.py"])


layout = html.Div(children=[
    html.Div(id='app-4-display-value'),
    #dcc.Location(id='url_', refresh=False),
    html.H1(children=['Запуск процесса сортировки']),

    daq.PowerButton(
        id='my-power-button',
        on=False,
        className='pwr_btn',
        color='Red',
        label='Запустить бота',
        size = 100,
        persistence=True,
    ),
    html.Div(id='power-button-output'),
    html.Div('Лог работы бота', id = 'text-header',
             style={'text-align':'center'}),
    dcc.Textarea(
        id='textarea-example',
        #value='Textarea content initialized\nwith multiple lines of text',
        style={'width': '100%', 'height': 200},
    ),
    dcc.Interval(
            id='interval-component_2',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
    ),
])


@app.callback(
    dash.dependencies.Output('power-button-output', 'children'),
    [dash.dependencies.Input('my-power-button', 'on')])
def update_output(on):
    global P
    status = 'Процесс не определен'
    if on==True:
        try:
            if P is None:
                P = thread_second()
                status = f'Процесс запущен: Pid {P.pid}'
        except BaseException as ex:
            print(ex)
    else:
        if isinstance(P, Popen):
            if P:
                P.terminate()
                status = f'Процесс pid: {P.pid} остановлен'
                P = None
    return status


@app.callback(
    Output('textarea-example', 'value'),
    Input('interval-component_2', 'n_intervals'),

)
def update_output(n_intervals):
    with open(settings.LOG_FILE_NAME,'r', encoding='utf-8') as file:
        lines = file.readlines()
        #lines = lines.reverse()
    lines = list(reversed(lines))

    lines = '\n'.join(lines[:10])
    return lines