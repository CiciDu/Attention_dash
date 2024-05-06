import numpy as np
import pandas as pd
import itertools
from numpy import random





def get_ts_for_each_combo_df(ts_obs_1_df, first_ts_obs_1_df, num_trial, ts_per_trial):
    '''
    Find ts_for_each_combo_df -- this df store specific information for each time step for each combo_id. 
    Important columns include: combo_id, ts, n_trial_ts_obs_1_any_order, n_rewarded_trial_ts_obs_1_any_order,
                            n_trial_ts_obs_1_first, n_rewarded_trial_ts_obs_1_first, 
                            
    '''
    first_ts_obs_1_df = first_ts_obs_1_df.copy()
    #first_ts_obs_1_df = furnish_first_ts_obs_1_df(first_ts_obs_1_df, num_trial, ts_per_trial)
    
    ts_obs_1_any_order_df = get_ts_obs_1_any_order_df(ts_obs_1_df)
    ts_obs_1_first_df = get_ts_obs_1_first_df(first_ts_obs_1_df)
    ts_for_each_combo_df = ts_obs_1_any_order_df.merge(ts_obs_1_first_df, on='ts', how='outer')

    # use merge to make the df contain all time steps 
    all_ts_df = pd.DataFrame(np.arange(1, ts_per_trial+1), columns=['ts'])
    ts_for_each_combo_df = ts_for_each_combo_df.merge(all_ts_df, on='ts', how='outer')
    ts_for_each_combo_df = ts_for_each_combo_df.fillna(0)

    return ts_for_each_combo_df



def get_ts_obs_1_any_order_df(ts_obs_1_df):
    '''
    This function returns a dataframe that contains the percentage of each time step to have obs=1, no matter if it's the first step to do so in the trial or not, 
    and also the percentage of successful trial out of all trial where the time step has obs=1.
    Important columns include: ts, n_trial_ts_obs_1_any_order, n_rewarded_trial_ts_obs_1_any_order
    '''
    ts_obs_1_df = ts_obs_1_df.copy()

    df = ts_obs_1_df.groupby(['ts']).count().reset_index()[['ts', 'trial']]
    df.rename(columns={'trial': 'n_trial_ts_obs_1_any_order'}, inplace=True)

    ts_obs_1_success_freq_df = ts_obs_1_df[ts_obs_1_df['condition'] >= 102].groupby(['ts']).count().reset_index()[['ts', 'trial']]
    ts_obs_1_success_freq_df.rename(columns={'trial': 'n_rewarded_trial_ts_obs_1_any_order'}, inplace=True)
    df = df.merge(ts_obs_1_success_freq_df[['ts', 'n_rewarded_trial_ts_obs_1_any_order']], on='ts', how='left')

    ts_obs_1_any_order_df = df
    return ts_obs_1_any_order_df


def get_ts_obs_1_first_df(first_ts_obs_1_df):
    '''
    This function returns a dataframe that contains the percentage of each time step to be the first time step to have obs=1.
    Important columns include: ts, n_trial_ts_obs_1_first, perc_trial_ts_obs_1_first, n_rewarded_trial_ts_obs_1_first, perc_rewarded_trial_ts_obs_1_first
    '''
    ts_obs_1_first_df = get_ts_obs_1_any_order_df(first_ts_obs_1_df)
    ts_obs_1_first_df.rename(columns={'n_trial_ts_obs_1_any_order': 'n_trial_ts_obs_1_first',
                                        'n_rewarded_trial_ts_obs_1_any_order': 'n_rewarded_trial_ts_obs_1_first'}, inplace=True) 
    
    return ts_obs_1_first_df



def add_more_info_to_ts_df(ts_for_each_combo_df, combo_id_df, all_high_attn_ts_for_each_combo_df, num_trial):
    # If the columns to be added already exist, drop them
    ts_for_each_combo_df = ts_for_each_combo_df.drop(columns=['success_rate', 'combo_num_trial', 'n_rewarded_trial_for_combo', 'attn_ts_counter'], errors='ignore')
    # Add columns like combo_success_rate, combo_num_trial, n_rewarded_trial_for_combo (those are combo-wide attributes)
    ts_for_each_combo_df = ts_for_each_combo_df.merge(combo_id_df[['combo_id', 'success_rate', 'ranking', 'n_rewarded_trial_for_combo', 'high_attn_ts_combo']], on='combo_id', how='left')
    ts_for_each_combo_df['combo_num_trial'] = num_trial

    # Then, let's add combo+ts specific attributes like attn_ts_counter
    ts_for_each_combo_df = ts_for_each_combo_df.merge(all_high_attn_ts_for_each_combo_df[['combo_id', 'ts', 'attn_ts_counter']], on=['combo_id', 'ts'], how='left')

    # Since ts_for_each_combo_df might contain more rows than all_high_attn_ts_for_each_combo_df (since it includes info of time steps that are not high-attention steps as well), we need to fill NA
    values = {"attn_ts_counter": -1}
    ts_for_each_combo_df = ts_for_each_combo_df.fillna(value=values)

    # Get some other columns
    # Now we want to get "perc_trial_ts_obs_1_any_order", which is the percentage of trial where the current time step has obs=1 no matter if it's the first time step to do so in the trial or no
    ts_for_each_combo_df['perc_trial_ts_obs_1_any_order'] = ts_for_each_combo_df['n_trial_ts_obs_1_any_order'] / num_trial  
    # We also want "perc_rewarded_trial_ts_obs_1_any_order", which is the percentage of successful trial out of all trial where the time step has obs=1
    ts_for_each_combo_df['perc_rewarded_trial_ts_obs_1_any_order'] = ts_for_each_combo_df['n_rewarded_trial_ts_obs_1_any_order'] / num_trial
    # Similarly, we want "perc_trial_ts_obs_1_first", which is the percentage of trials that the time step is the first to have obs=1, out of all trials
    ts_for_each_combo_df['perc_trial_ts_obs_1_first'] = ts_for_each_combo_df['n_trial_ts_obs_1_first'] / num_trial # number of trials that the time step is the first to have obs=1, out of all trials
    # And "perc_rewarded_trial_ts_obs_1_first", which is the percentage of successful trial out of all trial where the time step is the first to have obs=1
    ts_for_each_combo_df['perc_rewarded_trial_ts_obs_1_first'] = ts_for_each_combo_df['n_rewarded_trial_ts_obs_1_first'] / num_trial

    # Also get the percentage of trials that the time step is the first to have obs=1, out of all trials that have at least one time step with obs=1
    ts_for_each_combo_df['ratio_of_ts_obs_1_first_OVER_ts_obs_1_any_order'] = ts_for_each_combo_df['n_trial_ts_obs_1_first'] / ts_for_each_combo_df['n_trial_ts_obs_1_any_order']
    
    # make the following columns integer: 'n_trial_ts_obs_1_any_order', 'n_rewarded_trial_ts_obs_1_any_order', 'n_trial_ts_obs_1_first', 'n_rewarded_trial_ts_obs_1_first', 'attn_ts_counter'
    for column in ['ts', 'n_trial_ts_obs_1_any_order', 'n_rewarded_trial_ts_obs_1_any_order', 'n_trial_ts_obs_1_first', 'n_rewarded_trial_ts_obs_1_first', 'attn_ts_counter']:
        ts_for_each_combo_df[column] = ts_for_each_combo_df[column].astype(int)
        
    return ts_for_each_combo_df




