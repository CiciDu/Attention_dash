from methods.simulation_methods import simulation_class
from methods.dash_methods import dash_simul_helper_func
from methods.shared import dash_shared
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from dash import Dash, html, Input, State, Output, ctx
from dash.exceptions import PreventUpdate
import pandas as pd
import itertools
from numpy import random



def get_all_high_attn_ts_for_each_combo_df(combo_id_df, high_attn_ts_count, id_vars=['combo_id', 'success_rate', 'ranking', 'high_attn_ts_combo']):
    # get the percentage of each time step to be the first time step to have obs=1
    all_high_attn_ts_for_each_combo_df = combo_id_df.melt(id_vars=id_vars, 
                                        value_vars=['attn_time_' + str(i) for i in range(high_attn_ts_count)], 
                                        var_name='attn_ts_counter', value_name='ts')
    # change the values in all_high_attn_ts_for_each_combo_df['attn_ts_counter'] by extracting the number at the end of the string
    all_high_attn_ts_for_each_combo_df['attn_ts_counter'] = all_high_attn_ts_for_each_combo_df['attn_ts_counter'].str.extract('(\d+)').astype(int)
    all_high_attn_ts_for_each_combo_df.sort_values(by='ranking', ascending=True, inplace=True)

    return all_high_attn_ts_for_each_combo_df





def get_sampled_high_attn_time_steps_combo(ts_per_trial, high_attn_ts_count, max_high_attn_ts_combo=None):
    '''
    This function returns all possible combinations of high_attn_ts_count out of ts_per_trial
    If the number of possible combinations is too large, randomly sample max_high_attn_ts_combo of them
    '''

    # get all combinations of high_attn_ts_count out of ts_per_trial
    all_poss_high_attn_time_steps = list(itertools.combinations(range(1, ts_per_trial+1), high_attn_ts_count))
    all_poss_high_attn_time_steps = np.array(all_poss_high_attn_time_steps)
    # if the number of possible combinations is too large, randomly sample max_high_attn_ts_combo of them
    if (max_high_attn_ts_combo is not None):
        if len(all_poss_high_attn_time_steps) > max_high_attn_ts_combo:
            sampled_indices = random.choice(len(all_poss_high_attn_time_steps), max_high_attn_ts_combo, replace=False)
            sampled_high_attn_time_steps_combo = all_poss_high_attn_time_steps[sampled_indices]
            print("Sampled {} out of {} possible combinations".format(max_high_attn_ts_combo, len(all_poss_high_attn_time_steps)))
        else:
            sampled_high_attn_time_steps_combo = all_poss_high_attn_time_steps
            print("Using all {} possible combinations".format(len(all_poss_high_attn_time_steps)))
    else:
        sampled_high_attn_time_steps_combo = all_poss_high_attn_time_steps
        print("Using all {} possible combinations".format(len(all_poss_high_attn_time_steps)))
    return sampled_high_attn_time_steps_combo


