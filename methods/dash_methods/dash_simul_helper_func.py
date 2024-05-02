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




def put_down_high_level_inputs(input_items, simulation_params):
    children_count = dash_shared.create_children(input_items, simulation_params, 'count')
    children_probability = dash_shared.create_children(input_items, simulation_params, 'probability')

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

