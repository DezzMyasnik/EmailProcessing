import base64
import io

import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import init_db
from dash.dependencies import Output, Input, State
import plotly
from app import app
import dash
import dash_table as dt
import pandas as pd

df = pd.read_csv('Classyfy_.csv',sep=';')
classes = list(df['Class'].unique())
br =  [{'label': i, 'value': i} for i in classes]
PAGE_SIZE = 20
stat = df['Class'].value_counts()
#df_2 = stat.to_frame().reset_index().rename(columns={0:'Класс', 1:'Количество'})
df_2 = pd.DataFrame({'Класс':stat.index, 'Количество': stat.values} )
layout = html.Div(children=[
    html.Div(id='app-2-display-value'),
    html.H1(children='Работа с обучающей выборкой'),
    html.Div(children=[html.Button("Download CSV", id="btn_csv"), dcc.Download(id="download-dataframe-csv"),
                      ]),
    #dcc.Upload(id='upload-data', children=[html.Button('Upload File')]),
    #html.Div(id='output-data-upload'),

    dcc.Dropdown(
        id='dropdown',
        options=br,
        multi=False
    ),
    #html.Div(id='dd-output-container'),
    daq.NumericInput(
        id='my-numeric-input',
        value=PAGE_SIZE,
        max=30
    ),
    dt.DataTable(id='Table',
                 columns=[{"name": i, "id": i} for i in df.columns],
                 #data=df.to_dict('records'),
                 fill_width=True,

                 style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'textAlign': 'left',
                    },
                 style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                            },
                 page_current=0,
                 page_size=PAGE_SIZE,
                 page_action='custom',
                 editable=True,
                 #row_deletable=True
                #filter_action='custom',
                #filter_query='',
                 ),

    #html.Button('Add Row', id='editing-rows-button', n_clicks=0),
    html.P(),
    html.P(f'Длина обучающей выборки, записей: {df.shape[0]} ',style={'text-align':'center'}),
    dt.DataTable(id='table_of_classes_counts',
                 columns=[{"name": i, "id": i} for i in df_2.columns],
                 #fill_width=True,
                 style_cell={
                    #'whiteSpace': 'normal',
                    #'height': 'auto',
                    'textAlign': 'left',
                    },
                 style_table={
                     'width':'450px',
                     'position':'relative',
                     'left':'35%'
                 },
                 style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                            },
                 #page_current=0,
                 data =df_2.to_dict('records'),
                 )

])

#@app.callback(
#    Output('Table', 'data'),
#    Input('editing-rows-button', 'n_clicks'),
#    State('Table', 'data'),
#    State('Table', 'columns'))
#def add_row(n_clicks, rows, columns):
#    if n_clicks > 0:
#        rows.append({c['id']: '' for c in columns})
#    return rows


operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

"""
Загрузка файла с обучающей выборкой
"""
@app.callback(
    Output("download-dataframe-csv", "data"),
    Input("btn_csv", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    #df = pd.read_csv('Classyfy_.csv', sep=';')

    return dcc.send_file('Classyfy_.csv',filename='Classyfy_.csv')


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        else:
            # Assume that the user uploaded an excel file
            raise Exception
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

"""
Загрузка на сервер файла с обучающей выборкой
"""
@app.callback(Output('output-data-upload', 'children'),
              Input('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output_file(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


def split_filter_part(filter_part):
    for operator_type in operators:
        for operator in operator_type:
            if operator in filter_part:
                name_part, value_part = filter_part.split(operator, 1)
                name = name_part[name_part.find('{') + 1: name_part.rfind('}')]

                value_part = value_part.strip()
                v0 = value_part[0]
                if (v0 == value_part[-1] and v0 in ("'", '"', '`')):
                    value = value_part[1: -1].replace('\\' + v0, v0)
                else:
                    try:
                        value = float(value_part)
                    except ValueError:
                        value = value_part

                # word operators need spaces after them in the filter string,
                # but we don't want these later
                return name, operator_type[0].strip(), value

    return [None] * 3


@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown', 'value')])
def update_output(value):
    value = f"Выбрана категория '{value}'"
    return value

@app.callback(
    Output('Table', 'data'),
    Input('Table', "page_current"),
    Input('Table','page_size'),
    Input('dropdown', 'value'),
    #Input('editing-rows-button', 'n_clicks'),
    Input('my-numeric-input', 'value'),
    State('Table', 'data'),
    State('Table', 'columns'),

    #Input('Table', "filter_query")
)
def update_table(page_current,page_size,filter, pp_size,rows, columns): #filter
    PAGE_SIZE = pp_size
    page_size = PAGE_SIZE
    ctx = dash.callback_context
    if not ctx.triggered:
        control_id = 'No clicks yet'
    else:
        control_id = ctx.triggered[0]['prop_id'].split('.')[0]
   #print(control_id)
    if control_id == 'dropdown' or filter:
        return filtering_dash(filter, page_current, page_size)
    #elif control_id == 'editing-rows-button':
    #    if n_clicks > 0:
    #       rows.append({c['id']: '' for c in columns})
    #    return rows
    else:
        return df.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')


def filtering_dash(filter, page_current, page_size):
    if filter:
        filter = f"{'{Class}'} contains '{filter}'"
        #print(filter)
        filtering_expressions = filter.split(' && ')
        dff = df
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                dff = dff.loc[dff[col_name].str.contains(filter_value)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]

        return dff.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')
    else:
        return df.iloc[
               page_current * page_size:(page_current + 1) * page_size
               ].to_dict('records')


@app.callback(
    Output('app-2-display-value', 'children'),
    Input('app-2-dropdown', 'value'))
def display_value(value):
    return 'You have selected "{}"'.format(value)
