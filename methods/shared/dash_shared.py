import os
from turtle import st
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


def put_down_main_plot(fig, id='main_plot'):
    return html.Div([
        dcc.Loading(
            id="loading-1",
            type="default",
            children=html.Div(
                [
                    dcc.Graph(
                        id=id,
                        figure=fig
                    ),
                ], 
                style={
                    'width': '100%', 
                    'height': '150%',
                    'padding': '30px 0 0 0',
                    'display': 'flex',
                }
            )
        )
    ])

        
    


# def put_down_y_axis_variable(y, rank_to_start, rank_to_end, haha):
#     y_var = 'ranking' if y == 'ranking' else 'success rate'
#     return html.Div([
#         html.Div(
#             children=[
#                 html.Label(
#                     ['Y-axis variable:'], 
#                     style={'text-align': 'center', 
#                            'padding': '10px 10px 10px 10px'}
#                 ),
#                 dcc.Dropdown(
#                     id='y_var',
#                     options=['ranking', 'success rate'],
#                     value=y_var,
#                     searchable=False,
#                     multi=False,
#                     style={'width': '150px'},
#                 )
#             ],
#             style={'height': '30px', 'padding': '10px 10px 10px 10px', 'display': 'flex'}
#         ),
#         html.Div(
#             children=[
#                 html.Label(
#                     ['Rows to show:'], 
#                     style={'text-align': 'center', 
#                            'padding': '10px 10px 10px 10px'}
#                 ),
#                 dcc.Input(
#                     id='rank_to_start', 
#                     type="number", 
#                     placeholder=rank_to_start, 
#                     debounce=False,
#                     style={'width': '60px', 'height': '35px'},
#                     value=rank_to_start
#                 ),
#                 dcc.Dropdown(
#                     id='rank_to_end',
#                     options=['highest', 'lowest'],
#                     value='highest',
#                     searchable=False,
#                     multi=False,
#                     style={'width': '150px', 'height': '30px'},
#                 ),
#             ],
#             style={'height': '40px', 'padding': '10px 10px 10px 10px', 'display': 'flex'}
#         ),
#     ],
#     style={'padding': '5px 0px 10px 0px', 
#            'height': '50px',
#            'width': '700px', 
#            'background-color': '#B5D3E7', 
#            'display': 'flex',
#            'margin': '30px 0 10px 0',
#             },)



def create_error_massage_display():
    return html.Div(id='error_message',
                 children='Updated successfully',
                 style={'padding': '10px 10px 10px 10px', 'color': 'purple'})



def put_down_y_axis_variable(y, n_combo, rank_to_start=0, rank_to_end=10):

    y_var_choices = html.Div(
            children=[
                html.Label(
                    ['Y-axis variable:'], 
                    style={'text-align': 'center', 
                           'padding': '10px 10px 10px 10px'}
                ),
                dcc.Dropdown(
                    id='y_var',
                    options={
                            'ranking': 'ranking',
                            'success_rate': 'success rate',
                    },
                    value=y,
                    searchable=False,
                    multi=False,
                    style={'width': '150px'},
                )
                
            ],
            style={'height': '30px', 'padding': '10px 10px 10px 10px', 'display': 'flex'}
        )
    
    row_choices = html.Div(
            children=[
                html.Label(
                    id='n_combo',
                    children=[f"Display Ranks (out of {n_combo}):"], 
                    style={'text-align': 'center', 
                           'padding': '10px 10px 10px 10px'}
                ),
                dcc.Input(
                    id='rank_to_start', 
                    type="number", 
                    placeholder=rank_to_start, 
                    debounce=False,
                    style={'width': '60px', 'height': '35px'},
                    value=rank_to_start
                ),
                html.Label(
                    [' to '], 
                    style={'text-align': 'center', 
                           'padding': '10px 10px 10px 10px'}
                ),
                dcc.Input(
                    id='rank_to_end', 
                    type="number", 
                    placeholder=rank_to_end, 
                    debounce=False,
                    style={'width': '60px', 'height': '35px'},
                    value=rank_to_end
                ),
            ],
            style={'height': '40px', 'padding': '10px 10px 10px 10px', 'display': 'flex'}
        )

    return html.Div(children=[y_var_choices, row_choices],
                    style={'padding': '5px 0px 10px 0px', 
                        'height': '50px',
                        'width': '700px', 
                        'background-color': '#B5D3E7', 
                        'display': 'flex',
                        'margin': '30px 0 10px 0',
                            },)



def inspect_rank_to_start_and_rank_to_end(self, n_combo, rank_to_start, rank_to_end, default_rank_to_start, default_rank_to_end):
    if rank_to_start is None:
        rank_to_start = default_rank_to_start
    if rank_to_start == 0:
        rank_to_start = 1
    elif (rank_to_start >= 1) and (rank_to_start <= n_combo):
        rank_to_start = rank_to_start

    else:
        raise PreventUpdate(f"The number of row to start should be between 1 and {n_combo}.")

    if rank_to_end is None:
        rank_to_end = default_rank_to_end
    elif (rank_to_end > rank_to_start) and (rank_to_end <= n_combo):
        rank_to_end = rank_to_end
    else:
        raise PreventUpdate(f"The number of row to end should be between {rank_to_start} and {n_combo}.")
    return rank_to_start, rank_to_end
