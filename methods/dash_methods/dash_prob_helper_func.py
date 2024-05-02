from methods.dash_methods import dash_shared
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


def put_down_high_level_inputs(input_items, probability_params, including_high_attn_ts=True):
    if including_high_attn_ts:
        input_high_attn_ts = create_input_high_attn_ts(probability_params['high_attn_ts'])
        children = [input_high_attn_ts]
    else:
        children = []
    for item in input_items:
        children.append(dash_shared.create_input_div(item, probability_params))
    return html.Div(children,
                    style={'flex-direction': 'column', 
                            'justify-content': 'space-around', 
                            'display': 'flex', 
                            'padding': '10px 10px 10px 10px', 
                            'background-color': '#B5D3E7',
                            'margin': '0 0 10px 0',
                            'width': '630px'},
                    )


def create_input_high_attn_ts(high_attn_ts):
    high_attn_ts = ', '.join(map(str, high_attn_ts))
    return html.Div([
        html.Label('Current high attention time steps', style={'padding-right': '20px'}),  # Increased right padding
        dcc.Input(
            id="input_high_attn_ts",
            type='text',
            value=high_attn_ts,
            placeholder='',
            style={'width': '100px'},
        ),
    ], style={'display': 'flex', 'align-items': 'center', 'margin': '5px'}) 




def put_down_calculate_probability_button(id='calculate_probability_button'):
    return dash_shared.create_button(id, 'Calculate probability')


