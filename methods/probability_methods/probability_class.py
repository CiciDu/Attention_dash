from methods.simulation_methods import simulation_class, simulation_func, find_info_for_ts, find_info_for_combo
from methods.probability_methods import calc_prob_helper_func
from methods.plot_methods import plt_probability, plotly_probability
import numpy as np
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import random
import plotly.graph_objects as go


class Probability:


    def __init__(self) -> None:
        pass



    def calc_prob_for_all_combo_given_high_attn_ts_count(self, 
                                high_attn_ts_count=3,
                                ts_per_trial=9,
                                signal_dur = 3,
                                p_obs_1_high_attn_sig_pres = 0.8,
                                p_obs_1_high_attn_sig_abs = 0.2):
        
        self.high_attn_ts_count = high_attn_ts_count
        self.ts_per_trial = ts_per_trial
        self.signal_dur = signal_dur
        self.p_obs_1_high_attn_sig_pres = p_obs_1_high_attn_sig_pres
        self.p_obs_1_high_attn_sig_abs = p_obs_1_high_attn_sig_abs
        self.combo_id_df = calc_prob_helper_func.calc_prob_for_all_combo_given_high_attn_ts_count(high_attn_ts_count, ts_per_trial, signal_dur, 
                                                                                                p_obs_1_high_attn_sig_pres, p_obs_1_high_attn_sig_abs)
        self.process_important_df()


    def process_important_df(self):
        self.all_high_attn_ts_for_each_combo_df = calc_prob_helper_func.get_all_high_attn_ts_for_each_combo_df(self.combo_id_df,self.high_attn_ts_count)
        self.all_ts_for_each_combo_df = calc_prob_helper_func.get_all_ts_for_each_combo_df(self.combo_id_df, self.all_high_attn_ts_for_each_combo_df, self.ts_per_trial)

    
    def prepare_to_plot(self, n_combo_to_plot=10, highest_or_lowest='highest'):
        self.n_combo_to_plot = n_combo_to_plot
        self.highest_or_lowest = highest_or_lowest
        # Make a plot such that the x-axis shows the attention time steps, and the y-axis shows the success rate
        self.combo_id_df.sort_values(by='ranking', ascending=True, inplace=True)
        if highest_or_lowest == 'highest':
            self.combo_id_df_to_plot = self.combo_id_df.head(n_combo_to_plot)
        else:
            self.combo_id_df_to_plot = self.combo_id_df.tail(n_combo_to_plot)
        
        self.chosen_combo_id = self.combo_id_df_to_plot['combo_id'].unique()
        self.high_attn_ts_df_to_plot = self.all_high_attn_ts_for_each_combo_df[self.all_high_attn_ts_for_each_combo_df['combo_id'].isin(self.chosen_combo_id)]
        self.ts_to_plot = self.all_ts_for_each_combo_df[self.all_ts_for_each_combo_df['combo_id'].isin(self.chosen_combo_id)]



    def plot_probability_results(self, x='ts', y='ranking', hue='success_rate', show_plot=True):
        self.x = x
        self.y = y
        self.hue = hue
        self.fig, self.ax = plt_probability.plot_success_rate_of_many_combo(x=x, y=y, hue=hue, ts_to_plot=self.ts_to_plot, ts_per_trial=self.ts_per_trial, 
                                        n_combo_to_plot=self.n_combo_to_plot, highest_or_lowest=self.highest_or_lowest, show_plot=show_plot)




    def plot_probability_results_in_plotly(self, x='ts', y='ranking', color='success_rate', show_plot=True):
        self.x = x
        self.y = y
        self.color = color
        self.fig = plotly_probability.plot_success_rate_of_many_combo_in_plotly(x=x, y=y, color=color, ts_to_plot=self.ts_to_plot, ts_per_trial=self.ts_per_trial, 
                                        n_combo_to_plot=self.n_combo_to_plot, highest_or_lowest=self.highest_or_lowest, show_plot=show_plot)



