import dash_core_components as dcc
import dash_html_components as html
import init_db
from dash.dependencies import Output, Input
import plotly
from app import app
import dash
import dash_table as dt
import pandas as pd

df = pd.read_csv('Classyfy_.csv',sep=';')
classes = list(df['Class'].unique())
br =  [{'label': i, 'value': i} for i in classes]
PAGE_SIZE = 8
layout = html.Div(children=[
    html.Div(id='app-2-display-value'),
    dcc.Link('Перейти к Статистике сортировки', href='/apps/app1'),

    html.H1(children='Работа с обучающей выборкой'),

    html.Div(children='''
        Обучающая выборка
    '''),
    dcc.Dropdown(
        id='dropdown',
        options=br,

        multi=False
    ),
    html.Div(id='dd-output-container'),
    dt.DataTable(id='Table',
                 columns=[{"name": i, "id": i} for i in df.columns],
                 #data=df.to_dict('records'),

                 style_cell_conditional=[
                     {

                         'textAlign': 'left'
                     }
                 ],
                style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                            },
                page_current=0,
                page_size=PAGE_SIZE,
                page_action='custom',
                #filter_action='custom',
                #filter_query='',
                )

])

operators = [['ge ', '>='],
             ['le ', '<='],
             ['lt ', '<'],
             ['gt ', '>'],
             ['ne ', '!='],
             ['eq ', '='],
             ['contains '],
             ['datestartswith ']]

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
    Input('Table', "page_size"),
    Input('dropdown', 'value'),
    #Input('Table', "filter_query")
)
def update_table(page_current,page_size,filter ): #filter
    if filter:
        filter = f"{'{Class}'} contains '{filter}'"
        print(filter)
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
            page_current*page_size:(page_current+ 1)*page_size
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
