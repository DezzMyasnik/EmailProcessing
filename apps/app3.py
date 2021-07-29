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


with init_db.db_session:
    classes = list(init_db.distinct(o.detected_class for o in init_db.Emailflow))
    df = pd.read_sql('select * from Emailflow', init_db.db.get_connection())
    count=df.shape[0]
br =  [{'label': i, 'value': i} for i in classes]
PAGE_SIZE = 8
layout = html.Div(children=[
    html.Div(id='app-3-display-value'),
    html.H1(children='Результаты классификации'),

    dcc.Dropdown(
        id='dropdown_2',
        options=br,
        multi=True
    ),
    html.Div(id='dd-output-container_2'),
    dt.DataTable(id='result_of_classyfing_table',
                 columns=[{"name": i, "id": i} for i in df.columns],
                 #data=df.to_dict('records'),
                 style_cell={
                    'whiteSpace': 'normal',
                    'height': 'auto',
                    'textAlign': 'left',
                    },
                style_header={
                            'backgroundColor': 'rgb(230, 230, 230)',
                            'fontWeight': 'bold'
                            },
                #page_current = int(count/PAGE_SIZE)-1,
                #page_size = PAGE_SIZE,
                #page_action = 'custom',
                #editable = True,
                #row_deletable = True,


                #filter_action='custom',
                #filter_query='',
                ),
    dcc.Interval(
            id='interval-component_2',
            interval=5 * 1000,  # in milliseconds
            n_intervals=0
        )
    #html.Button('Add Row', id='editing-rows-button', n_clicks=0),

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
    dash.dependencies.Output('dd-output-container_2', 'children'),
    [dash.dependencies.Input('dropdown_2', 'value')])
def update_output(value):
    value = f"Выбрана категория '{value}'"
    return value



@app.callback(
    Output('result_of_classyfing_table', 'data'),
    Input('result_of_classyfing_table', "page_current"),
    Input('result_of_classyfing_table', "page_size"),
    Input('dropdown_2', 'value'),
    Input('interval-component_2', 'n_intervals')
)
def update_table(page_current,page_size,filter,n): #filter
    with init_db.db_session:
        df = pd.read_sql('select * from Emailflow', init_db.db.get_connection())
        count = df.shape[0]
        br = [{'label': i, 'value': i} for i in df]
    #page_size = pp_size
    return filtering_dash(filter, page_current, page_size)




def filtering_dash(filter, page_current, page_size):
    with init_db.db_session:
        df = pd.read_sql('select * from Emailflow', init_db.db.get_connection())
    if filter:
        if len(filter)>1:
            filt_contains = filter
            filter = ' && '.join([f"{'{detected_class}'} contains '{item}'" for item in filter])
        else:
            filter = f"{'{detected_class}'} contains '{filter[0]}'"
        print(filter)
        filtering_expressions = filter.split(' && ')
        dff = df
        for filter_part in filtering_expressions:
            col_name, operator, filter_value = split_filter_part(filter_part)

            if operator in ('eq', 'ne', 'lt', 'le', 'gt', 'ge'):
                # these operators match pandas series operator method names
                dff = dff.loc[getattr(dff[col_name], operator)(filter_value)]
            elif operator == 'contains':
                if len(filtering_expressions)==1:
                    dff = dff.loc[dff[col_name].str.contains(filter_value)]
                else:
                    dff = dff.loc[dff[col_name].isin(filt_contains)]
            elif operator == 'datestartswith':
                # this is a simplification of the front-end filtering logic,
                # only works with complete fields in standard format
                dff = dff.loc[dff[col_name].str.startswith(filter_value)]
        return dff.sort_values(by=['id'],ascending=False).to_dict('records')
        #return dff.iloc[
        #       page_current * page_size:(page_current + 1) * page_size
        #       ].sort_values(by=['id'],ascending=False).to_dict('records')
    else:

            return df.sort_values(by=['id'],ascending=False).iloc[:20].to_dict('records')
        #return df.iloc[
         #      page_current * page_size:(page_current + 1) * page_size
         #      ].sort_values(by=['id'],ascending=False).to_dict('records')