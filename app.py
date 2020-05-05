from process_data import store_relational_JH_data
import os
from flask import Flask
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import numpy as np

import dash

dash.__version__

# from get_data import get_johns_hopkins
print(os.getcwd())

# get_johns_hopkins()
confirmed = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
df_confirmed = store_relational_JH_data(confirmed, 'confirmed')
deaths = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
df_deaths = store_relational_JH_data(deaths, 'deaths')
recovered = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv'
df_recovered = store_relational_JH_data(recovered, 'recovered')

#df_confirmed = pd.read_csv('COVID_relational_confirmed.csv')
#df_deaths = pd.read_csv('COVID_relational_deaths.csv')
#df_recovered = pd.read_csv('COVID_relational_recovered.csv')

fig = go.Figure()
app = dash.Dash(__name__)
server = app.server
app.layout = html.Div([

    dcc.Markdown('''
    #  COVID-19 Visualization
	'''),

    dcc.Markdown('''
    Data is taken from Johns Hopkins, COVID-19 GitHub Repository: https://github.com/CSSEGISandData/COVID-19
	'''),

    dcc.Markdown('''
    ## Multi-Select Country for visualization
    '''),

    dcc.Dropdown(
        id='country_drop_down',
        options=[{'label': each, 'value': each}
                 for each in df_confirmed['country'].unique()],
        value=['US', 'Italy', 'Spain'],  # which are pre-selected
        multi=True
    ),

    dcc.Markdown('''
        ## Select Y - Scale: Linear or Logarithmic
        '''),

    dcc.Dropdown(
        id='y_scale',
        options=[
            {'label': 'Linear Scale', 'value': 'linear'},
            {'label': 'Logarithmic Scale', 'value': 'log'},
        ],
        value='linear',
        multi=False
    ),

    dcc.Graph(figure=fig, id='confirmed'),
    dcc.Graph(figure=fig, id='death'),
    dcc.Graph(figure=fig, id='recovered'),

    dcc.Markdown('''
    ### Author: Siddhant Sapte
    - [LinkedIn](https://www.linkedin.com/in/siddhant-sapte/)
    - [GitHub](https://github.com/SiddSapte12)
    ''')
])


@app.callback(
    [Output('confirmed', 'figure'), Output(
        'death', 'figure'), Output('recovered', 'figure')],
    [Input('country_drop_down', 'value'), Input('y_scale', 'value')])
def update_figure(country_list, scale):
    if 'linear' in scale:
        c_yaxis = {'type': "linear",
                   'title': 'Confirmed infected people (source johns hopkins csse, linear-scale)'
                   }
        d_yaxis = {'type': "linear",
                   'title': 'Confirmed deaths (source johns hopkins csse, linear-scale)'
                   }
        r_yaxis = {'type': "linear",
                   'title': 'Confirmed recovered people (source johns hopkins csse, linear-scale)'
                   }
    else:
        c_yaxis = {'type': "log",
                   'title': 'Confirmed infected people (source johns hopkins csse, log-scale)'
                   }
        d_yaxis = {'type': "log",
                   'title': 'Confirmed deaths (source johns hopkins csse, log-scale)'
                   }
        r_yaxis = {'type': "log",
                   'title': 'Confirmed recovered people (source johns hopkins csse, log-scale)'
                   }

    traces_c = []
    traces_d = []
    traces_r = []
    for each in country_list:
        df_confi = df_confirmed[df_confirmed['country'] == each]
        df_c = df_confi.groupby(['country', 'date']).agg(np.sum).reset_index()

        df_dea = df_deaths[df_deaths['country'] == each]
        df_d = df_dea.groupby(['country', 'date']).agg(np.sum).reset_index()

        df_reco = df_recovered[df_recovered['country'] == each]
        df_r = df_reco.groupby(['country', 'date']).agg(np.sum).reset_index()

        traces_c.append(dict(
            x=df_c.date, y=df_c['confirmed'], mode='markers+lines', opacity=0.9, name=each))
        traces_d.append(dict(
            x=df_d.date, y=df_d['deaths'], mode='markers+lines', opacity=0.9, name=each))
        traces_r.append(dict(
            x=df_r.date, y=df_r['recovered'], mode='markers+lines', opacity=0.9, name=each))

    c = {
        'data': traces_c,
        'layout': dict(
            width=1500,
            height=520,

            xaxis={'title': 'Timeline',
                   'tickangle': -45,
                   'nticks': 20,
                   'tickfont': dict(size=14, color="#7f7f7f"),
                   },

            yaxis=c_yaxis,
            title='Total Confirmed Cases (per Million)<br>(Hover for more Info)'
        )
    }

    d = {
        'data': traces_d,
        'layout': dict(
            width=1500,
            height=520,

            xaxis={'title': 'Timeline',
                   'tickangle': -45,
                   'nticks': 20,
                   'tickfont': dict(size=14, color="#7f7f7f"),
                   },

            yaxis=d_yaxis,
            title='Total Deaths (per Million)<br>(Hover for more Info)'
        )
    }

    r = {
        'data': traces_r,
        'layout': dict(
            width=1500,
            height=520,

            xaxis={'title': 'Timeline',
                   'tickangle': -45,
                   'nticks': 20,
                   'tickfont': dict(size=14, color="#7f7f7f"),
                   },

            yaxis=r_yaxis,
            title='Total Recovered Cases (per Million)<br>(Hover for more Info)'
        )
    }

    return c, d, r


if __name__ == '__main__':
    app.run_server(debug=True)
