import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app1, app2, app3, app4, app5

""""
             children=[
        html.Ul(id ='ul_menu',children=[
            html.Li(children=dcc.Link('Перейти к Статистике сортировки', href='/apps/app1')),
            html.Li(children=dcc.Link('Перейти к обучающей выборке', href='/apps/app2')),
            html.Li(children=dcc.Link('Перейти к результатам классификации', href='/apps/app3')),
            ]),

    ] """


menu_li = [html.Li(className='menu-children', children=[dcc.Link('К статистике', href='/apps/app1')]),
           html.Li(className='menu-children', children=[dcc.Link('К обучающей выборке', href='/apps/app2')]),
           html.Li(className='menu-children', children=[dcc.Link('К водопаду писем', href='/apps/app3')]),
           html.Li(className='menu-children', children=[dcc.Link('К управлению ботом', href='/apps/app4')]),
           #html.Li(className='menu-children', children=[dcc.Link('К настройкам', href='/apps/app5')])
           ]

app.layout = html.Div(children=[
    dcc.Location(id='url', refresh=False),

    html.Footer(id='menu',
                children=[html.Ul(className='main-menu',
                            children=menu_li
                                      )
                              ]
                    ),

    html.Div(id='page-content'),
    ])


@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/apps/app1':
        app.layout
        return app1.layout
    elif pathname == '/apps/app2':
        return app2.layout
    elif pathname == '/apps/app3':
        return app3.layout
    elif pathname == '/apps/app4':
        return app4.layout
    elif pathname == '/apps/app5':
        return app5.layout
    elif pathname == '/':
       return app4.layout
    else:
        return '404'

if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=False, port=8050)