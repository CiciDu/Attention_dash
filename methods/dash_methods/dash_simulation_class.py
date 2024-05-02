from methods.simulation_methods import simulation_class
from methods.dash_methods import dash_simul_helper_func, dash_shared
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, Input, State, Output, ctx
from dash.exceptions import PreventUpdate
import pandas as pd


# https://dash.plotly.com/interactive-graphing




class DashSimulation(simulation_class.Simulation):



    def __init__(self):
        super().__init__()
        self.generate_input_items()



    def generate_simulation_params(self):
        self.simulation_params = {'num_trial': self.num_trial,
                                'max_high_attn_ts_combo': self.max_high_attn_ts_combo,
                                'ts_per_trial': self.ts_per_trial,
                                'high_attn_ts_count': self.high_attn_ts_count,
                                'signal_dur': self.signal_dur,
                                'p_obs_1_high_attn_sig_pres': self.p_obs_1_high_attn_sig_pres,
                                'p_obs_1_high_attn_sig_abs': self.p_obs_1_high_attn_sig_abs,
                                'p_obs_1_low_attn_sig_pres': self.p_obs_1_low_attn_sig_pres,
                                'p_obs_1_low_attn_sig_abs': self.p_obs_1_low_attn_sig_abs}  

        self.simulation_params_default = self.simulation_params.copy()     
        self.default_n_combo_to_plot = self.n_combo_to_plot



    def generate_input_items(self):
        # Set the displayed name and the range for the input values
        self.input_items = {'count': [['num_trial', 'Trial count', 1, 1000000],
                                    ['max_high_attn_ts_combo', 'Max high-attention time step combos', 1, 10000],
                                    ['ts_per_trial', 'Time steps per trial', 1, 10000],
                                    ['high_attn_ts_count', 'High-attention time steps per trial', 1, 'ts_per_trial'],
                                    ['signal_dur', 'Signal duration', 1, 'ts_per_trial']],
                    'probability': [['p_obs_1_high_attn_sig_pres', 'cp. of obs = 1 w signal w attention', 0, 1],
                                    ['p_obs_1_high_attn_sig_abs', 'cp. of obs = 1 w/o signal w attention', 0, 1],
                                    ['p_obs_1_low_attn_sig_pres', 'cp. of obs = 1 w signal w/o attention', 0, 1],
                                    ['p_obs_1_low_attn_sig_abs', 'cp. of obs = 1 w/o signal w/o attention', 0, 1]]}

        self.input_names = [item[0] for item in self.input_items['count'] + self.input_items['probability']]
        self.input_displayed_names = [item[1] for item in self.input_items['count'] + self.input_items['probability']]
        self.min_values = [item[2] for item in self.input_items['count'] + self.input_items['probability']]
        self.max_values = [item[3] for item in self.input_items['count'] + self.input_items['probability']]


    # def update_max_values(self):
    #     self.max_values = [item[3] for item in self.input_items['count'] + self.input_items['probability']]
    #     # check the element in max_values. If it is a string, replace it with the value of the corresponding input
    #     for i in range(len(self.max_values)):
    #         if isinstance(self.max_values[i], str):
    #             self.max_values[i] = self.simulation_params[self.max_values[i]]
        

    def prepare_dash_for_main_plots_layout(self, id_prefix=''):
        self.id_prefix = id_prefix
        self.generate_simulation_params()
        
        return html.Div([
                        dash_simul_helper_func.put_down_high_level_inputs(self.input_items, self.simulation_params),
                        dash_shared.put_down_run_simulation_button(),
                        dash_shared.put_down_y_axis_variable(self.y, self.n_combo_to_plot, self.highest_or_lowest),
                        #dash_shared.put_down_refresh_plot_button(),
                        dash_shared.put_down_main_plot(self.fig),
                        ])


    def make_dash_for_main_plots(self):

        external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

        self.app = Dash(__name__, external_stylesheets=external_stylesheets)
        self.app.layout = self.prepare_dash_for_main_plots_layout()

        self.make_functions_to_update(self.app)

        #self.app.run(debug=True)
        #self.app.run_server(port=8051)
        return


    def make_functions_to_update(self, app):
        self.make_function_to_run_simulation(app)
        self.make_function_to_refresh_plot(app)
        return
    


    def make_function_to_run_simulation(self, app):
        @app.callback(
            Output("main_plot", "figure", allow_duplicate=True),
            Input("run_simulation_button", "n_clicks"),
            [State("input_{}".format(item[0]), "value") for item in self.input_items['count']] +
            [State("input_{}".format(item[0]), "value") for item in self.input_items['probability']],
            prevent_initial_call=True,
        )
        def run_simulation(n_clicks, *vals):

            for i in range(len(self.input_names)):
                if vals[i] is not None:
                    # Check if the value is within the range [min_value, max_value]
                    min_value = self.min_values[i]
                    max_value = self.max_values[i]
                    if isinstance(max_value, str):
                        max_value = self.simulation_params[max_value]

                    if min_value <= vals[i] <= max_value:
                        self.simulation_params[self.input_names[i]] = vals[i]
                    else:
                        # raise an error message
                        print("Error: The value for {} should be between {} and {}. No update was made".format(self.input_displayed_names[i], min_value, max_value))
                        raise PreventUpdate("The value for {} is out of range. Please enter a value between {} and {}".format(self.input_names[i], min_value, max_value))
                else:
                    # If the value is None, set it to the default value
                    self.simulation_params[self.input_names[i]] = self.simulation_params_default[self.input_names[i]]


            print("Running simulation with the following parameters:")
            print(self.simulation_params)
            self.run_simulation(**self.simulation_params)

            self.plot_simulation_again()

            return self.fig
        return





    def make_function_to_refresh_plot(self, app):
        @app.callback(
            Output("main_plot", "figure", allow_duplicate=True),
            Input("y_var", "value"),
            Input("n_combo_to_plot", "value"),
            Input("highest_or_lowest", "value"),
            prevent_initial_call=True
        )
        def refresh_plot(y_var, n_combo_to_plot, highest_or_lowest):
            self.y = 'ranking' if y_var == 'ranking' else 'success_rate'
            self.n_combo_to_plot = n_combo_to_plot
            if n_combo_to_plot is None:
                self.n_combo_to_plot = self.default_n_combo_to_plot
            elif n_combo_to_plot < 1:
                self.n_combo_to_plot = n_combo_to_plot
            self.highest_or_lowest = highest_or_lowest
            self.plot_simulation_again()
            
            return self.fig
        return 





    def plot_simulation_again(self):
        self.prepare_to_plot(n_combo_to_plot=self.n_combo_to_plot, highest_or_lowest=self.highest_or_lowest)
        self.plot_simulation_results_in_plotly(x=self.x,
                                    y=self.y,
                                    hue_var=self.hue_var,
                                    hue_denominator=self.hue_denominator, 
                                    hue_numerator=self.hue_numerator,
                                    show_plot=False)
        
