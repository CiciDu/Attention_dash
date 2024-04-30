from methods.simulation_methods import find_info_for_ts
import numpy as np
import pandas as pd
import itertools
from numpy import random



def simulate_results_for_one_combo_of_high_attn_time_steps(high_attn_time_steps, num_trial, ts_per_trial, signal_dur, 
                                        p_obs_1_high_attn_sig_pres, p_obs_1_high_attn_sig_abs, 
                                        p_obs_1_low_attn_sig_pres, p_obs_1_low_attn_sig_abs):
    '''
    This function simulates the results for one combination of attention time steps

    Parameters
    ----------
    high_attn_time_steps: 
        the time steps where the subject is attending to the signal

    num_trial: int
        the number of trial to simulate
    ts_per_trial: int
        the number of time steps in the trial
    high_attn_ts_per_trial: int
        the number of time steps that the subject is attending to the signal
    signal_dur: int
        the duration of the signal (# time steps)
    p_obs_1_high_attn_sig_pres: float (denoted by h in the document)
        the probability of observing a signal when the subject is attending to the signal
    p_obs_1_high_attn_sig_abs: float (denoted by 1-c in the document)
    '''

    # sample signal_start_time for all trial
    signal_start_time = random.choice(ts_per_trial, num_trial)+1 # use +1 because the time step starts from 1

    # get the time step conditions for all trial, signaling whether signal is present and whether attention is paid
    ts_conditions = get_ts_conditions(num_trial, ts_per_trial, high_attn_time_steps, signal_dur, signal_start_time)

    # replace the value with the correct probability. 
    p_obs_thold = get_p_obs_thold(ts_conditions, ts_per_trial, p_obs_1_high_attn_sig_pres, p_obs_1_high_attn_sig_abs, p_obs_1_low_attn_sig_pres, p_obs_1_low_attn_sig_abs)

    # sample the signal observation by getting random numbers between 0 and 1. We take 1 minus the random number to get the probability of observing signal
    p_obs_sampled = random.rand(num_trial, ts_per_trial)

    # get all the time steps that have their obs = 1
    ts_obs_1_df = get_ts_obs_1_df(p_obs_sampled, p_obs_thold, ts_conditions)

    # get the first time step where the observation exceeds the threshold
    first_ts_obs_1_df = ts_obs_1_df.groupby('trial').first().reset_index(drop=False)

    # get the percentage of each time step to be the first time step to have obs=1
    ts_for_each_combo_df = find_info_for_ts.get_ts_for_each_combo_df(ts_obs_1_df, first_ts_obs_1_df, num_trial, ts_per_trial)

    # take out the rows where the time step is within the signal time steps
    success_df = first_ts_obs_1_df[first_ts_obs_1_df['condition'] >= 102]
    if len(success_df) > 0:
        # calculate the percentage of successes among all trial
        success_rate = len(success_df)/num_trial
        # Among the successes, calculate the percentage of high attention and low attention
        high_attn_success_rate = len(success_df[success_df['condition'] == 103])/len(success_df)
        low_attn_success_rate = len(success_df[success_df['condition'] == 102])/len(success_df)
    else:
        success_rate = 0
        high_attn_success_rate = 0
        low_attn_success_rate = 0


    result_from_one_combo = {'n_trial_w_obs_1': len(ts_obs_1_df['trial'].unique()),
                      'n_rewarded_trial_for_combo': len(success_df),
                       'combo_success_rate': success_rate, 
                       'high_attn_success_rate': high_attn_success_rate, 
                       'low_attn_success_rate': low_attn_success_rate,
                       'ts_for_each_combo_df': ts_for_each_combo_df}

    return result_from_one_combo



def get_sampled_high_attn_time_steps_combo(ts_per_trial, high_attn_ts_per_trial, max_high_attn_ts_combo=None):
    '''
    This function returns all possible combinations of high_attn_ts_per_trial out of ts_per_trial
    If the number of possible combinations is too large, randomly sample max_high_attn_ts_combo of them
    '''

    # get all combinations of high_attn_ts_per_trial out of ts_per_trial
    all_poss_high_attn_time_steps = list(itertools.combinations(range(1, ts_per_trial+1), high_attn_ts_per_trial))
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



def get_ts_conditions(num_trial, ts_per_trial, high_attn_time_steps, signal_dur, signal_start_time):
    '''
    This function returns a 2D array where each row represents the time step conditions for each trial

    The value of each element in the array is determined by the following rules:
    100: no signal, no attention
    101: no signal, attention
    102: signal, no attention
    103: signal, attention
    ''' 


    # get the time steps where signal is present for all trial
     # note that the elements in signal_time_steps might exceed ts_per_trial. We shall deal with that later
    signal_time_steps = np.tile(np.arange(signal_dur), (num_trial, 1)) + signal_start_time.reshape(-1, 1) 
    # get the probability of observing signal for each time step
     # notes that here we pretend each trial has ts_per_trial + signal_dur time steps (equal to the number of columns of p_obs_thold). Later we will ignore the extra steps
    # To start with, assign 100 to all time steps. 0 means no signal and no attention
    ts_conditions = np.repeat(100, num_trial*(ts_per_trial+signal_dur)).reshape(num_trial, ts_per_trial+signal_dur)
    # Add 1 if attention is paid. 
    ts_conditions[np.arange(num_trial)[:, None], high_attn_time_steps-1] += 1
    # Add 2 if signal is present. Consequently, the value will be 103 if both signal is present and attention is paid
    ts_conditions[np.arange(num_trial)[:, None], signal_time_steps-1] += 2
    # we use -1 because the time step starts from 1 in high_attn_time_steps and signal_time_steps


    return ts_conditions



def get_p_obs_thold(ts_conditions, ts_per_trial, p_obs_1_high_attn_sig_pres, p_obs_1_high_attn_sig_abs, p_obs_1_low_attn_sig_pres, p_obs_1_low_attn_sig_abs):
    '''
    This function replaces the value in ts_conditions with the corresponding observation probability thold
    '''

    # First make a copy of ts_conditions
    p_obs_thold = np.array(ts_conditions, copy=True, dtype=float)
    p_obs_thold[p_obs_thold == 103] = p_obs_1_high_attn_sig_pres
    p_obs_thold[p_obs_thold == 102] = p_obs_1_low_attn_sig_pres 
    p_obs_thold[p_obs_thold == 101] = p_obs_1_high_attn_sig_abs
    p_obs_thold[p_obs_thold == 100] = p_obs_1_low_attn_sig_abs

    # now we truncate the extra columns in p_obs_thold
    p_obs_thold = p_obs_thold[:, :ts_per_trial]
    return p_obs_thold



def get_ts_obs_1_df(p_obs_sampled, p_obs_thold, ts_conditions):
    '''
    This function returns a dataframe that contains the time steps where the observation exceeds the thold
    '''

    # compare the signal observation with the thold and put the result into a dataframe
    # notice that we use <= here because we want to include the time step where the random number is within the threshold of probability
    ts_obs_1 = np.where(p_obs_sampled <= p_obs_thold)
    ts_obs_1_df = pd.DataFrame(ts_obs_1).T
    ts_obs_1_df.columns = ['trial', 'ts']
    ts_obs_1_df['condition'] = ts_conditions[ts_obs_1_df['trial'], ts_obs_1_df['ts']]
    ts_obs_1_df['ts'] = ts_obs_1_df['ts'] + 1 # after getting conditions, we use +1 because the time step starts from 1

    return ts_obs_1_df







