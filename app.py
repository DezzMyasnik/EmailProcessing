import dash
import os
external_scripts = [
    'https://www.google-analytics.com/analytics.js',
    {'src': 'https://cdn.polyfill.io/v2/polyfill.min.js'},
    {
        'src': 'https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.10/lodash.core.js',
        'integrity': 'sha256-Qqd/EfdABZUcAxjOkMi8eGEivtdTkh3b65xCZL4qAQA=',
        'crossorigin': 'anonymous'
    }
]



# external CSS stylesheets
abs_f= os.path.abspath("assets/style.css")
#external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', abs_f]
external_stylesheets = ['http://127.0.0.1:8050/apps/style_2.css']

app = dash.Dash(__name__,
                external_scripts=external_scripts,
                #external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

#app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=external_stylesheets)
server = app.server