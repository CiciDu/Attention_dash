from methods.probability_methods import calc_prob_helper_func, probability_class
from methods.dash_methods import dash_prob_helper_func, dash_simul_helper_func
from methods.shared import dash_shared
from methods.plot_methods import plotly_probability
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, Input, State, Output, ctx, dcc
from dash.exceptions import PreventUpdate
import pandas as pd


# https://dash.plotly.com/interactive-graphing


class DashProbability(probability_class.Probability):

    def __init__(self):

        
        self.generate_input_items()
        super().__init__()




    def prepare_to_use_dash(self,                                             
                            high_attn_ts_count=3,
                            ts_per_trial=9,
                            signal_dur = 3,
                            p_obs_1_high_attn_sig_pres = 0.8,
                            p_obs_1_high_attn_sig_abs = 0.2,
                            rank_to_start=0, 
                            rank_to_end=15):
        self.x = 'ts'
        self.y = 'ranking'
        self.color = 'success_rate'
        self.rank_to_start = rank_to_start
        self.rank_to_end = rank_to_end
        self.default_rank_to_start = rank_to_start
        self.default_rank_to_end = rank_to_end
        self.probability_params = {'high_attn_ts_count': high_attn_ts_count,
                                'ts_per_trial': ts_per_trial,
                                'signal_dur': signal_dur,
                                'p_obs_1_high_attn_sig_pres': p_obs_1_high_attn_sig_pres,
                                'p_obs_1_high_attn_sig_abs': p_obs_1_high_attn_sig_abs} 
        self.probability_params_default = self.probability_params.copy()
        self.calculate_probability_anew_and_plot()
    
        #self.shared.inspect_rank_to_start_and_rank_to_end(rank_to_start, rank_to_end)


    def prepare_dash_for_main_plots_layout(self, 
                                            id_prefix='',):
        self.id_prefix = id_prefix  

        return html.Div([
                        dash_shared.create_error_massage_display(),
                        dash_prob_helper_func.put_down_high_level_inputs(self.input_items, self.probability_params, including_high_attn_ts=False),
                        dash_prob_helper_func.put_down_calculate_probability_button(),
                        dash_shared.put_down_y_axis_variable(self.y, self.n_combo, self.rank_to_start, self.rank_to_end),
                        dash_shared.put_down_refresh_plot_button(),
                        dash_shared.put_down_main_plot(self.fig),
                        
                        ])



    def make_dash_for_main_plots(self):

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        self.app = Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.layout = self.prepare_dash_for_main_plots_layout()
        # self.app.layout = dcc.Loading(
        #     id="loading-1",
        #     type="default",
        #     children=self.prepare_dash_for_main_plots_layout())

        self.make_function_to_calc_prob_for_all_combo_given_high_attn_ts_count(self.app)
        self.make_function_to_refresh_plot(self.app)

        #self.app.run(debug=True)
        #self.app.run_server(port=8080)
        return



    def generate_input_items(self):

        self.input_items = [['high_attn_ts_count', 'High attention time steps', 0, 'ts_per_trial'],
                            ['ts_per_trial', 'Time steps per trial', 1, 10000],
                            ['signal_dur', 'Signal duration', 1, 10000],
                            ['p_obs_1_high_attn_sig_pres', 'prob. of obs = 1 w signal w attention', 0, 1],
                            ['p_obs_1_high_attn_sig_abs', 'prob. of obs = 1 w/o signal w attention', 0, 1]]
        self.input_names = [item[0] for item in self.input_items]
        self.input_displayed_names = [item[1] for item in self.input_items]
        self.min_values = [item[2] for item in self.input_items]
        self.max_values = [item[3] for item in self.input_items]
        return



    def calculate_probability_anew_and_plot(self):
        self.calc_prob_for_all_combo_given_high_attn_ts_count(**self.probability_params)
        self.prepare_to_plot(rank_to_start=self.rank_to_start, rank_to_end=self.rank_to_end)
        self.plot_probability_results_in_plotly(x=self.x, y=self.y, color=self.color, show_plot=False)
        return


    def make_function_to_calc_prob_for_all_combo_given_high_attn_ts_count(self, app):
        @app.callback(
            Output("main_plot", "figure", allow_duplicate=True),
            Output("error_message", "children", allow_duplicate=True),
            Output("n_combo", "children"),
            Input("calculate_probability_button", "n_clicks"),
            [State("input_{}".format(item[0]), "value") for item in self.input_items],
            prevent_initial_call=True,
        )
        def calculate_probability_after_update(n_clicks, *vals):
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
                            print("Error: The value for {} should be between {} and {}. No update was made".format(self.input_displayed_names[i], min_value, max_value))
                            raise PreventUpdate("The value for {} is out of range. Please enter a value between {} and {}".format(self.input_names[i], min_value, max_value))
                    else:
                        # If the value is None, set it to the default value
                        self.probability_params[self.input_names[i]] = self.probability_params_default[self.input_names[i]]

                print("Running probability with the following parameters:")
                print(self.probability_params)
                self.calculate_probability_anew_and_plot()
                n_combo_text = f"Display Ranks (out of {self.n_combo}):"

                return self.fig, "Updated successfully", n_combo_text
            except Exception as e:
                n_combo_text = f"Display Ranks (out of {self.n_combo}):"
                return self.fig, f"An error occurred. No update was made. Error: {e}", n_combo_text
        return



    def make_function_to_refresh_plot(self, app):
        # this is identical with the function in dash_simulation_class
        @app.callback(
            Output("main_plot", "figure", allow_duplicate=True),
            Output("error_message", "children", allow_duplicate=True),
            Input('refresh_plot_button', 'n_clicks'),
            State("y_var", "value"),
            State("rank_to_start", "value"),
            State("rank_to_end", "value"),
            prevent_initial_call=True
        )
        def refresh_plot(n_clicks, y_var, rank_to_start, rank_to_end):
            try:
                self.y = y_var
                self.rank_to_start, self.rank_to_end = dash_shared.inspect_rank_to_start_and_rank_to_end(self, self.n_combo, rank_to_start, rank_to_end, self.default_rank_to_start, self.default_rank_to_end)

                self.prepare_to_plot(rank_to_start=self.rank_to_start, rank_to_end=self.rank_to_end)
                self.plot_probability_results_in_plotly(x=self.x, y=self.y, color=self.color, show_plot=False)
    
                return self.fig, "Updated successfully"
            except Exception as e:
                return self.fig, f"An error occurred. No update was made. Error: {e}"
        return 
    
