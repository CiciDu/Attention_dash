from methods.simulation_methods import simulation_class
from methods.dash_methods import dash_simul_helper_func
from methods.shared import dash_shared
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, Input, State, Output, ctx
from dash.exceptions import PreventUpdate
import pandas as pd




class SharedClass:

    def __init__(self):
        pass


    def prepare_to_plot(self, rank_to_start=1, rank_to_end=15):
        if rank_to_start >= rank_to_end:
            raise ValueError("rank_to_start must be less than rank_to_end")
        self.rank_to_start = rank_to_start
        self.rank_to_end = rank_to_end
        self.n_combo = len(self.combo_id_df)
        # Make a plot such that the x-axis shows the attention time steps, and the y-axis shows the success rate
        self.combo_id_df.sort_values(by='ranking', ascending=True, inplace=True)
        self.combo_id_df_to_plot = self.combo_id_df[self.combo_id_df['ranking'].between(rank_to_start, rank_to_end)].copy()
        self.chosen_combo_id = self.combo_id_df_to_plot['combo_id'].unique()
        self.high_attn_ts_df_to_plot = self.all_high_attn_ts_for_each_combo_df[self.all_high_attn_ts_for_each_combo_df['ranking'].between(rank_to_start, rank_to_end)]
        # self.ts_to_plot = self.all_ts_for_each_combo_df[self.all_ts_for_each_combo_df['combo_id'].isin(self.chosen_combo_id)]
        self.ts_to_plot = self.all_ts_for_each_combo_df[self.all_ts_for_each_combo_df['ranking'].between(rank_to_start, rank_to_end)]
        if len(self.ts_to_plot) == 0:
            raise ValueError("No data to plot. Please check the rank_to_start and rank_to_end values.")



