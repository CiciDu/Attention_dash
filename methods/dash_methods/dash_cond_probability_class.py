from methods.probability_methods import calc_prob_helper_func, probability_class
from methods.dash_methods import dash_prob_helper_func
from methods.plot_methods import plotly_probability
from methods.shared import dash_shared
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, Input, State, Output, ctx
from dash.exceptions import PreventUpdate
import pandas as pd


# https://dash.plotly.com/interactive-graphing


class DashCondProbability():

    def __init__(self):
        self.probability_params_default = dict(high_attn_ts = [],
                            ts_per_trial = 9,
                            signal_dur = 3,
                            p_obs_1_high_attn_sig_pres = 0.8, # h
                            p_obs_1_high_attn_sig_abs = 0.2)
        self.generate_input_items()



    def generate_input_items(self):

        self.input_items = [['ts_per_trial', 'Time steps per trial', 1, 10000],
                            ['signal_dur', 'Signal duration', 1, 10000],
                            ['p_obs_1_high_attn_sig_pres', 'prob. of obs = 1 w signal w attention', 0, 1],
                            ['p_obs_1_high_attn_sig_abs', 'prob. of obs = 1 w/o signal w attention', 0, 1]]
        self.input_names = [item[0] for item in self.input_items]
        self.input_displayed_names = [item[1] for item in self.input_items]
        self.min_values = [item[2] for item in self.input_items]
        self.max_values = [item[3] for item in self.input_items]
        return



    def calculate_probability(self, 
                            high_attn_ts = [5, 8],
                            ts_per_trial = 9,
                            signal_dur = 3,
                            p_obs_1_high_attn_sig_pres = 0.8, # h
                            p_obs_1_high_attn_sig_abs = 0.2):
        
        self.probability_params = {'high_attn_ts': high_attn_ts,
                                'ts_per_trial': ts_per_trial,
                                'signal_dur': signal_dur,
                                'p_obs_1_high_attn_sig_pres': p_obs_1_high_attn_sig_pres,
                                'p_obs_1_high_attn_sig_abs': p_obs_1_high_attn_sig_abs}
                                       
        # if any item in self.probability_params is None, then we replace it by the default
        for key, value in self.probability_params.items():
            if value is None:
                self.probability_params[key] = self.probability_params_default[key]                     
        
        self.adding_ts_result_df = calc_prob_helper_func.calc_prob_after_adding_to_existing_high_attn_ts(**self.probability_params)
        pass


    
    def plot_probability_in_plotly(self, show_plot=True):
        self.fig = plotly_probability.plot_success_rate_after_adding_to_high_attn_ts(self.adding_ts_result_df, high_attn_ts=self.probability_params['high_attn_ts'], show_plot=show_plot)


    def prepare_dash_for_main_plots_layout(self, id_prefix=''):
        self.id_prefix = id_prefix   
        
        return html.Div([
                        dash_shared.create_error_massage_display(),
                        dash_prob_helper_func.put_down_high_level_inputs(self.input_items, self.probability_params),
                        dash_prob_helper_func.put_down_calculate_probability_button(),
                        dash_shared.put_down_main_plot(self.fig),
                        ])


    def make_dash_for_main_plots(self):

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        self.app = Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.layout = self.prepare_dash_for_main_plots_layout()

        self.make_function_to_calculate_probability(self.app)

        #self.app.run(debug=True)
        #self.app.run_server(port=8080)
        return




    def make_function_to_calculate_probability(self, app):
        @app.callback(
            Output("main_plot", "figure", allow_duplicate=True),
            Output("error_message", "children", allow_duplicate=True),
            Input("calculate_probability_button", "n_clicks"),
            State("input_high_attn_ts", "value"),
            [State("input_{}".format(item[0]), "value") for item in self.input_items],
            prevent_initial_call=True,
        )
        def calculate_probability(n_clicks, high_attn_ts, *vals):
            try:
                # updtate the probability_params with the new values
                for i in range(len(self.input_names)):
                    if vals[i] is not None:
                        # Check if the value is within the range [min_value, max_value]
                        min_value = self.min_values[i]
                        max_value = self.max_values[i]
                        if isinstance(max_value, str):
                            max_value = self.probability_params[max_value]
                        if min_value <= vals[i] <= max_value:
                            self.probability_params[self.input_names[i]] = vals[i]
                        else:
                            # raise an error message
                            print("Error: The value for {} should be between {} and {}. No update was made.".format(self.input_displayed_names[i], min_value, max_value))
                            raise PreventUpdate("The value for {} is out of range. Please enter a value between {} and {}.".format(self.input_names[i], min_value, max_value))
                    else:
                        # If the value is None, set it to the default value
                        self.probability_params[self.input_names[i]] = self.probability_params_default[self.input_names[i]]

                # update the high_attn_ts
                self.update_high_attn_ts(high_attn_ts)

                print("Running probability with the following parameters:")
                print(self.probability_params)
                self.calculate_probability(**self.probability_params)
                self.plot_probability_in_plotly(show_plot=False)
                return self.fig, "Updated successfully"
            except Exception as e:
                return self.fig, f"An error occurred. No update was made. Error: {e}"
        
        return



    def update_high_attn_ts(self, high_attn_ts):
        # Check if the high_attn_ts is in the right format
        if isinstance(high_attn_ts, str):
            if len(high_attn_ts) == 0:
                high_attn_ts = []
            else:
                try:
                    high_attn_ts = [int(i) for i in high_attn_ts.split(', ')]
                except ValueError:
                    print("Error: The value for high attention time steps is not in the correct format. No update was made. Please separate every two integers by a comma and a space, if more than one value is entered.")
                    raise PreventUpdate("The value for high attention time steps is not in the correct format. Please enter a value in the correct format")
        else:
            print("Error: The value for high attention time steps is not in the correct format. No update was made")
            raise PreventUpdate("The value for high attention time steps is not in the correct format. Please enter a value in the correct format")
        

        # Check if the values are within the range [0, ts_per_trial]
        ts_max_value = self.probability_params['ts_per_trial']
        for elem in high_attn_ts:
            if not 0 <= elem <= ts_max_value:
                # raise an error message
                print("Error: The value for high attention time steps should be between 0 and {}. No update was made".format(ts_max_value))
                raise PreventUpdate("The value for high attention time steps should be between 0 and {}. Please enter a value between 0 and {}".format(ts_max_value, ts_max_value))
        
        # If all is correct, update the high_attn_ts in the probability_params
        self.probability_params['high_attn_ts'] = high_attn_ts
        
        return
