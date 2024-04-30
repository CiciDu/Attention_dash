import os
import numpy as np
import matplotlib
from matplotlib import rc
import matplotlib.pyplot as plt
import pandas as pd
from dash import html, dcc
import pandas as pd
import plotly.graph_objects as go
import matplotlib, random
from dash import Input, Output, State
from dash.exceptions import PreventUpdate


plt.rcParams["animation.html"] = "html5"
os.environ['KMP_DUPLICATE_LIB_OK']='True'
rc('animation', html='jshtml')
matplotlib.rcParams.update(matplotlib.rcParamsDefault)
matplotlib.rcParams['animation.embed_limit'] = 2**128
pd.set_option('display.float_format', lambda x: '%.5f' % x)
np.set_printoptions(suppress=True)

# drop down: https://dash.plotly.com/dash-core-components/dropdown

# input: https://dash.plotly.com/dash-core-components/input

# callback_context: https://dash.plotly.com/advanced-callbacks


def create_input_div(item, simulation_params):
    return html.Div([
        html.Label(item[1], style={'padding-right': '20px'}),  # Increased right padding
        dcc.Input(
            id="input_{}".format(item[0]),
            type='number',
            value=simulation_params[item[0]],
            placeholder=simulation_params[item[0]],
            style={'width': '100px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin': '5px'})  # Added margin



def create_children(input_items, simulation_params, key):
    children = []
    for item in input_items[key]:
        children.append(create_input_div(item, simulation_params))
    return children



def put_down_high_level_inputs(input_items, simulation_params):
    children_count = create_children(input_items, simulation_params, 'count')
    children_probability = create_children(input_items, simulation_params, 'probability')

    return html.Div([html.Div(children_count), 
                     html.Div(children_probability)],
                    style={'flex-direction': 'column', 
                            'justify-content': 'space-around', 
                            'display': 'flex', 
                            'padding': '10px 10px 10px 10px', 
                            'background-color': '#B5D3E7', 
                            'margin': '0 0 10px 0',
                            'width': '630px'},
                    )

def create_button(id, button_name):
    return html.Button(button_name, id=id, n_clicks=0, 
                        style={
                            'width': '50%', 
                            'background-color': '#7fa982', 
                            'padding': '10px 10px 10px 10px', 
                            'justifyContent': 'center',
                            'alignItems': 'center',                            
                            'display': 'flex',
                            'margin':'auto'
                        })

def put_down_run_simulation_button(id='run_simulation_button'):
    return create_button(id, 'Rerun simulation')



def put_down_refresh_plot_button(id='refresh_plot_button'):
    return create_button(id, 'Refresh plot')



def put_down_y_axis_variable(y, n_combo_to_plot, highest_or_lowest):
    y_var = 'ranking' if y == 'success_rate_ranking' else 'success rate'
    return html.Div([
        html.Div(
            children=[
                html.Label(
                    ['Y-axis variable:'], 
                    style={'text-align': 'center', 
                           'padding': '10px 10px 10px 10px'}
                ),
                dcc.Dropdown(
                    id='y_var',
                    options=['ranking', 'success rate'],
                    value=y_var,
                    searchable=False,
                    multi=False,
                    style={'width': '150px'},
                )
            ],
            style={'height': '30px', 'padding': '10px 10px 10px 10px', 'display': 'flex'}
        ),
        html.Div(
            children=[
                html.Label(
                    ['Rows to show:'], 
                    style={'text-align': 'center', 
                           'padding': '10px 10px 10px 10px'}
                ),
                dcc.Input(
                    id='n_combo_to_plot', 
                    type="number", 
                    placeholder=n_combo_to_plot, 
                    debounce=False,
                    style={'width': '60px', 'height': '35px'},
                    value=n_combo_to_plot
                ),
                dcc.Dropdown(
                    id='highest_or_lowest',
                    options=['highest', 'lowest'],
                    value=highest_or_lowest,
                    searchable=False,
                    multi=False,
                    style={'width': '150px', 'height': '30px'},
                ),
            ],
            style={'height': '40px', 'padding': '10px 10px 10px 10px', 'display': 'flex'}
        ),
    ],
    style={'padding': '5px 0px 10px 0px', 
           'height': '50px',
           'width': '700px', 
           'background-color': '#B5D3E7', 
           'display': 'flex',
           'margin': '30px 0 10px 0',
            },)




def put_down_main_plot(fig, id='main_plot'):
    return html.Div([
                dcc.Graph(
                    id=id,
                    figure=fig),
            ], style={'width': '100%', 
                      'padding': '30px 0 0 0',
                      'display': 'flex',
                    })

