from methods.simulation_methods import simulation_func, find_info_for_ts, find_info_for_combo
from methods.plot_methods import plt_simulation, plotly_simulation
import numpy as np
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import random
import plotly.graph_objects as go


class Simulation:


    def __init__(self) -> None:
        pass



    def run_simulation(self,
                        ts_per_trial=9,
                        high_attn_ts_count=3,
                        max_high_attn_ts_combo=20,
                        num_trial = 1000,
                        signal_dur = 3,
                        p_obs_1_high_attn_sig_pres = 0.7,
                        p_obs_1_high_attn_sig_abs = 0.3,
                        p_obs_1_low_attn_sig_pres = 0.2,
                        p_obs_1_low_attn_sig_abs = 0.1,
    ):
        self.sample_time_steps_combo(ts_per_trial=ts_per_trial, high_attn_ts_count=high_attn_ts_count, max_high_attn_ts_combo=max_high_attn_ts_combo)
        self.simulate_for_sampled_combo(num_trial=num_trial, signal_dur=signal_dur,
                                        p_obs_1_high_attn_sig_pres=p_obs_1_high_attn_sig_pres,
                                        p_obs_1_high_attn_sig_abs=p_obs_1_high_attn_sig_abs,
                                        p_obs_1_low_attn_sig_pres=p_obs_1_low_attn_sig_pres,
                                        p_obs_1_low_attn_sig_abs=p_obs_1_low_attn_sig_abs)
        self.process_important_df()
        #return self.combo_id_df, self.all_high_attn_ts_for_each_combo_df, self.all_ts_for_each_combo_df



    def sample_time_steps_combo(self, ts_per_trial=9, high_attn_ts_count=3, max_high_attn_ts_combo=20):
        self.ts_per_trial = ts_per_trial
        self.high_attn_ts_count = high_attn_ts_count
        self.max_high_attn_ts_combo = max_high_attn_ts_combo
        self.sampled_high_attn_time_steps_combo = simulation_func.get_sampled_high_attn_time_steps_combo(ts_per_trial, high_attn_ts_count, max_high_attn_ts_combo=max_high_attn_ts_combo)



    def simulate_for_sampled_combo(self, 
                                num_trial = 1000,
                                signal_dur = 3,
                                p_obs_1_high_attn_sig_pres = 0.7,
                                p_obs_1_high_attn_sig_abs = 0.3,
                                p_obs_1_low_attn_sig_pres = 0.2,
                                p_obs_1_low_attn_sig_abs = 0.1):
        
        self.num_trial = num_trial
        self.signal_dur = signal_dur
        self.p_obs_1_high_attn_sig_pres = p_obs_1_high_attn_sig_pres
        self.p_obs_1_high_attn_sig_abs = p_obs_1_high_attn_sig_abs
        self.p_obs_1_low_attn_sig_pres = p_obs_1_low_attn_sig_pres
        self.p_obs_1_low_attn_sig_abs = p_obs_1_low_attn_sig_abs


        dict_of_all_results = {'success_rate': [], 'high_attn_success_rate': [], 'low_attn_success_rate': [], 'n_trial_w_obs_1': [], 'n_rewarded_trial_for_combo': []}

        for i in range(self.sampled_high_attn_time_steps_combo.shape[0]):
            # sample the set of time instances where the agent pays attention
            if i % 10 == 0:
                print("Simulating attention combo {} out of {}".format(i, self.sampled_high_attn_time_steps_combo.shape[0]))
            high_attn_time_steps = self.sampled_high_attn_time_steps_combo[i, :]
            result_from_one_combo = simulation_func.simulate_results_for_one_combo_of_high_attn_time_steps(high_attn_time_steps, num_trial, self.ts_per_trial, signal_dur, 
                                                p_obs_1_high_attn_sig_pres, p_obs_1_high_attn_sig_abs, 
                                                p_obs_1_low_attn_sig_pres, p_obs_1_low_attn_sig_abs)

            for metrics in dict_of_all_results.keys():
                dict_of_all_results[metrics].append(result_from_one_combo[metrics])

            ts_for_each_combo_df = result_from_one_combo['ts_for_each_combo_df']
            ts_for_each_combo_df['combo_id'] = i
            if i == 0:
                all_ts_for_each_combo_df = ts_for_each_combo_df
            else:
                all_ts_for_each_combo_df = pd.concat([all_ts_for_each_combo_df, ts_for_each_combo_df])
        print('Simulation completed')
        # store all result information into a df, along with attn_combo information
        # columns including combo_id, success_rate, num_trial, high_attn_success_rate, low_attn_success_rate, and the attn_time_# columns, etc
        self.combo_id_df = find_info_for_combo.get_combo_id_df(self.sampled_high_attn_time_steps_combo, dict_of_all_results, num_trial)
        self.all_ts_for_each_combo_df = all_ts_for_each_combo_df           


    def process_important_df(self):
        # Note: the difference between all_high_attn_ts_for_each_combo_df and all_ts_for_each_combo_df is that the former contains only the information of high-attn ts for each combo, but the latter contains all time steps for each combo
        self.all_high_attn_ts_for_each_combo_df = self.combo_id_df.melt(id_vars=['combo_id', 'success_rate', 'ranking', 'high_attn_success_rate', 'low_attn_success_rate', 'n_rewarded_trial_for_combo', 'high_attn_ts_combo'], 
                                            value_vars=['attn_time_' + str(i) for i in range(self.high_attn_ts_count)], 
                                            var_name='attn_ts_counter', value_name='ts')
        # change the values in all_high_attn_ts_for_each_combo_df['attn_ts_counter'] by extracting the number at the end of the string
        self.all_high_attn_ts_for_each_combo_df['attn_ts_counter'] = self.all_high_attn_ts_for_each_combo_df['attn_ts_counter'].str.extract('(\d+)').astype(int)
        self.all_ts_for_each_combo_df = find_info_for_ts.add_more_info_to_ts_df(self.all_ts_for_each_combo_df, self.combo_id_df, self.all_high_attn_ts_for_each_combo_df, self.num_trial)

        #return self.combo_id_df, self.all_high_attn_ts_for_each_combo_df, self.all_ts_for_each_combo_df
    

    def prepare_to_plot(self, n_combo_to_plot=10, highest_or_lowest='highest'):
        self.n_combo_to_plot = n_combo_to_plot
        self.highest_or_lowest = highest_or_lowest
        # Make a plot such that the x-axis shows the attention time steps, and the y-axis shows the success rate
        if highest_or_lowest == 'highest':
            self.combo_id_df_to_plot = self.combo_id_df.head(n_combo_to_plot)
        else:
            self.combo_id_df_to_plot = self.combo_id_df.tail(n_combo_to_plot)
        
        self.chosen_combo_id = self.combo_id_df_to_plot['combo_id'].unique()
        self.high_attn_ts_df_to_plot = self.all_high_attn_ts_for_each_combo_df[self.all_high_attn_ts_for_each_combo_df['combo_id'].isin(self.chosen_combo_id)]
        # Find the corresponding rows in ts_for_each_combo_df
        self.ts_to_plot = self.all_ts_for_each_combo_df[self.all_ts_for_each_combo_df['combo_id'].isin(self.chosen_combo_id)]
        
        #return self.combo_id_df_to_plot, self.high_attn_ts_df_to_plot, self.ts_to_plot
    




    def plot_simulation_results(self, x='ts', y='ranking', hue_var=None, hue_denominator='n_trial_ts_obs_1_first', hue_numerator='n_rewarded_trial_ts_obs_1_first', show_plot=True):
        self.x = x
        self.y = y
        self.hue_var = hue_var
        self.hue_denominator = hue_denominator
        self.hue_numerator = hue_numerator

        self.fig, self.ax = plt_simulation.plot_simulation_results(x=x, y=y, hue_var=hue_var, hue_denominator=hue_denominator, hue_numerator=hue_numerator,
                                    ts_to_plot=self.ts_to_plot, ts_per_trial=self.ts_per_trial, n_combo_to_plot=self.n_combo_to_plot, 
                                    highest_or_lowest=self.highest_or_lowest, show_plot=show_plot)



    def plot_simulation_results_in_plotly(self, x='ts', y='ranking', hue_var=None, hue_denominator='n_trial_ts_obs_1_first', hue_numerator='n_rewarded_trial_ts_obs_1_first', show_plot=True):
        self.x = x
        self.y = y
        self.hue_var = hue_var
        self.hue_denominator = hue_denominator
        self.hue_numerator = hue_numerator

        self.fig = plotly_simulation.plot_simulation_results_in_plotly(x=x, y=y, hue_var=hue_var, hue_denominator=hue_denominator, hue_numerator=hue_numerator,
                                    ts_to_plot=self.ts_to_plot, ts_per_trial=self.ts_per_trial, 
                                    n_combo_to_plot=self.n_combo_to_plot, highest_or_lowest=self.highest_or_lowest, show_plot=show_plot)






