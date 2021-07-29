import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_table as dt
import settings
from app import app
def create_list(listing):
    li_list = [html.Li(children=item) for item in settings.droped_emails]
    return li_list

layout = html.Div(
    children=[
        html.Div('Список адресатов не требующих ответа'),
        html.Div(children=[dcc.Input(id='input-adress', type='email'),
                           html.Button('Добавить',n_clicks=0,id='add-btn', ),]),

        html.Ul(id ='list_of_droped_emails',
                children=[html.Li(id ='list_of_item',)]),
        html.Div('Database settings'),

    ]
)

@app.callback(
    dash.dependencies.Output('list_of_item', 'children'),
    [dash.dependencies.Input('add-btn', 'n_clicks')],
    [dash.dependencies.State('input-adress', 'value')])
def update_output(n_clicks, value):
    settings.droped_emails.append(value)
    value = settings.droped_emails

    return create_list(value)
