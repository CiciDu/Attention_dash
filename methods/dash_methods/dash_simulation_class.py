from methods.simulation_methods import simulation_class
from methods.dash_methods import dash_simul_helper_func
from methods.shared import dash_shared
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
        



    def prepare_to_use_dash(self, ts_per_trial=9, 
                            high_attn_ts_count=2, 
                            max_high_attn_ts_combo=100,
                            num_trial=10000,
                            signal_dur=3,
                            p_obs_1_high_attn_sig_pres=0.8,
                            p_obs_1_high_attn_sig_abs=0.2,
                            p_obs_1_low_attn_sig_pres=0,
                            p_obs_1_low_attn_sig_abs=0,
                            rank_to_start=0,
                            rank_to_end=15):
        
        self.generate_input_items()
        self.sample_time_steps_combo(ts_per_trial=ts_per_trial, high_attn_ts_count=high_attn_ts_count, max_high_attn_ts_combo=max_high_attn_ts_combo)
        self.simulate_for_sampled_combo(num_trial=num_trial, signal_dur=signal_dur,
                                        p_obs_1_high_attn_sig_pres=p_obs_1_high_attn_sig_pres,
                                        p_obs_1_high_attn_sig_abs=p_obs_1_high_attn_sig_abs,
                                        p_obs_1_low_attn_sig_pres=p_obs_1_low_attn_sig_pres,
                                        p_obs_1_low_attn_sig_abs=p_obs_1_low_attn_sig_abs)

        self.process_important_df()
        self.prepare_to_plot(rank_to_start=rank_to_start, rank_to_end=rank_to_end)
        self.plot_simulation_results_in_plotly(x='ts',
                                    #y='success_rate',
                                    y='ranking',
                                    hue_var='perc_rewarded_trial_ts_obs_1_any_order',
                                    show_plot=False)
        self.generate_simulation_params()
        self.prepare_dash_for_main_plots_layout()


    def prepare_dash_for_main_plots_layout(self, id_prefix=''):
        self.id_prefix = id_prefix
        
        return html.Div([
                        dash_simul_helper_func.put_down_high_level_inputs(self.input_items, self.simulation_params),
                        dash_shared.put_down_run_simulation_button(),
                        dash_shared.put_down_y_axis_variable(self.y, self.n_combo, self.rank_to_start, self.rank_to_end),
                        dash_shared.put_down_refresh_plot_button(),
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
        self.default_rank_to_start = self.rank_to_start
        self.default_rank_to_end = self.rank_to_end



    def generate_input_items(self):
        # Set the displayed name and the range for the input values
        self.input_items = {'count': [['num_trial', 'Trial count', 1, 1000000],
                                    ['max_high_attn_ts_combo', 'Max high-attention time step combos', 1, 10000],
                                    ['ts_per_trial', 'Time steps per trial', 1, 10000],
                                    ['high_attn_ts_count', 'High-attention time steps per trial', 1, 'ts_per_trial'],
                                    ['signal_dur', 'Signal duration', 1, 'ts_per_trial']],
                    'probability': [['p_obs_1_high_attn_sig_pres', 'prob. of obs = 1 w signal w attention', 0, 1],
                                    ['p_obs_1_high_attn_sig_abs', 'prob. of obs = 1 w/o signal w attention', 0, 1],
                                    ['p_obs_1_low_attn_sig_pres', 'prob. of obs = 1 w signal w/o attention', 0, 1],
                                    ['p_obs_1_low_attn_sig_abs', 'prob. of obs = 1 w/o signal w/o attention', 0, 1]]}

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
            Input('refresh_plot_button', 'n_clicks'),
            State("y_var", "value"),
            State("rank_to_start", "value"),
            State("rank_to_end", "value"),
            prevent_initial_call=True
        )
        def refresh_plot(n_clicks, y_var, rank_to_start, rank_to_end):
            self.y = 'ranking' if y_var == 'ranking' else 'success_rate'
            self.rank_to_start, self.rank_to_end = dash_shared.inspect_rank_to_start_and_rank_to_end(self, self.n_combo, rank_to_start, rank_to_end, self.default_rank_to_start, self.default_rank_to_end)


            self.plot_simulation_again()
            
            return self.fig
        return 





    def plot_simulation_again(self):
        self.prepare_to_plot(rank_to_start=self.rank_to_start, rank_to_end=self.rank_to_end)
        self.plot_simulation_results_in_plotly(x=self.x,
                                    y=self.y,
                                    hue_var=self.hue_var,
                                    hue_denominator=self.hue_denominator, 
                                    hue_numerator=self.hue_numerator,
                                    show_plot=False)
        
