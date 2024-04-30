import numpy as np
import pandas as pd
import itertools
from numpy import random


def get_combo_id_df(sampled_high_attn_time_steps_combo, dict_of_all_results, num_trial):
    '''
    This function returns a dataframe that contains info for each combo_id.
    Columns includes: combo_id, success_rate, num_trial, n_rewarded_trial_for_combo, high_attn_success_rate, low_attn_success_rate, and the attn_time_# columns
    '''

    high_attn_ts_per_trial = sampled_high_attn_time_steps_combo.shape[1]
    combo_id_df = pd.DataFrame(sampled_high_attn_time_steps_combo, columns=['attn_time_' + str(i) for i in range(high_attn_ts_per_trial)]) 
    combo_id_df['combo_id'] = np.arange(sampled_high_attn_time_steps_combo.shape[0])
    combo_id_df['num_trial'] = num_trial
    for column in dict_of_all_results.keys():
        combo_id_df[column] = dict_of_all_results[column]

    combo_id_df.sort_values(by='combo_success_rate', ascending=False, inplace=True)
    combo_id_df['success_rate_ranking'] = np.arange(combo_id_df.shape[0])+1
    combo_id_df.reset_index(drop=True, inplace=True)

    combo_id_df['high_attn_ts_combo'] = combo_id_df[['attn_time_' + str(i) for i in range(high_attn_ts_per_trial)]].values.tolist()
    return combo_id_df