from methods.shared import methods_shared
import itertools
import seaborn as sns
import os
import warnings
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import math
from math import pi
from matplotlib import rc
from numpy import random




def get_all_ts_for_each_combo_df(combo_id_df, all_high_attn_ts_for_each_combo_df, ts_per_trial):

    # for ts_for_each_combo_df, we want to make sure that for each combo_id, it contains all ts, not just the high-attn ones
    all_ts_for_each_combo_df = pd.DataFrame(list(itertools.product(range(1, ts_per_trial+1), range(combo_id_df.shape[0]))), columns=['ts', 'combo_id'])
    # add the success rate to all_ts_for_each_combo_df
    all_ts_for_each_combo_df = all_ts_for_each_combo_df.merge(combo_id_df[['combo_id', 'success_rate', 'ranking', 'high_attn_ts_combo']], on=['combo_id'], how='left')
    # merge to add the note for high-attn ts
    all_ts_for_each_combo_df = all_ts_for_each_combo_df.merge(all_high_attn_ts_for_each_combo_df[['combo_id', 'ts', 'attn_ts_counter']], on=['combo_id', 'ts'], how='left')
    # fill NA with False
    all_ts_for_each_combo_df['attn_ts_counter'] = all_ts_for_each_combo_df['attn_ts_counter'].fillna(-1)
    all_ts_for_each_combo_df.sort_values(by='ranking', ascending=True, inplace=True)

    return all_ts_for_each_combo_df


def calc_prob_for_all_combo_given_high_attn_ts_count(high_attn_ts_count, 
                                                     ts_per_trial, signal_dur, 
                                                    p_obs_1_high_attn_sig_pres, p_obs_1_high_attn_sig_abs
):
        

    all_high_attn_time_steps_combo = methods_shared.get_sampled_high_attn_time_steps_combo(ts_per_trial, high_attn_ts_count, max_high_attn_ts_combo=None)


    combo_id_df = pd.DataFrame(columns=['combo_id', 'success_rate'] +
                                        ['attn_time_' + str(i) for i in range(high_attn_ts_count)])

    for i in range(all_high_attn_time_steps_combo.shape[0]):
        # sample the set of time instances where the agent pays attention
        if i % 100 == 0:
            print("Calculate probability for attention combo {} out of {}".format(i, all_high_attn_time_steps_combo.shape[0]))
        high_attn_time_steps = all_high_attn_time_steps_combo[i, :]


        success_rate_of_one_combo = calc_prob_given_high_attn_ts_positions(high_attn_ts=high_attn_time_steps, ts_per_trial=ts_per_trial,
                                                                            signal_dur=signal_dur, p_obs_1_high_attn_sig_pres=p_obs_1_high_attn_sig_pres,
                                                                        p_obs_1_high_attn_sig_abs=p_obs_1_high_attn_sig_abs)

        combo_id_df.loc[i, 'combo_id'] = i
        combo_id_df.loc[i, 'success_rate'] = success_rate_of_one_combo
        combo_id_df.loc[i, ['attn_time_' + str(i) for i in range(high_attn_ts_count)]] = high_attn_time_steps      
    
    combo_id_df['ranking'] = combo_id_df['success_rate'].rank(ascending=False, method='first').astype(int)
    combo_id_df['high_attn_ts_combo'] = combo_id_df[['attn_time_' + str(i) for i in range(high_attn_ts_count)]].values.tolist()
    combo_id_df.sort_values(by='ranking', ascending=True, inplace=True)
    return combo_id_df





# The below assumes that ts starts from 1
def calc_prob_given_high_attn_ts_positions(high_attn_ts = [1, 2, 3],
                                            ts_per_trial = 9,
                                            signal_dur = 3,
                                            p_obs_1_high_attn_sig_pres = 0.8, # h
                                            p_obs_1_high_attn_sig_abs = 0.2, # c
):
    # first check if the high_attn_ts is within the bound of [1, ts_per_trial]
    if (max(high_attn_ts) > ts_per_trial) or (min(high_attn_ts) < 1):
        raise ValueError('The high_attn_ts is out of bound of ts_per_trial')
    # check if the high_attn_ts is within the signal duration

    # for any position of signal start
    accum_prob = 0
    for j in range(1, ts_per_trial+1):
        high_attn_ts = np.array(high_attn_ts).reshape(-1)
        # find the overlap between high-attn ts and signal duration
        order_of_high_attn_ts_in_S = np.where((high_attn_ts >= j) & (high_attn_ts <= (j+signal_dur-1)))[0]
        if len(order_of_high_attn_ts_in_S) == 0:
            continue
        else:
            # find sigma_ (the index of the first high-attn ts that overlaps with signal duration)
            order_of_high_attn_ts_in_S = order_of_high_attn_ts_in_S + 1 # use +1 because we start from 1
            sigma_ = order_of_high_attn_ts_in_S[0]
            # find lambda_ (the index of the last high-attn ts that overlaps with signal duration)
            lambda_ = order_of_high_attn_ts_in_S[-1]
            # for mu to be any number between sigma_ and lambda_
            for mu in range(sigma_, lambda_+1):
                p_succ = (1-p_obs_1_high_attn_sig_abs)**(sigma_-1) * \
                        (1-p_obs_1_high_attn_sig_pres)**(mu-sigma_)* \
                        p_obs_1_high_attn_sig_pres
                accum_prob += p_succ
    accum_prob = accum_prob/ts_per_trial
    return accum_prob





# The below assumes that ts starts from 1 instead of 0.
def calc_expected_prob_given_high_attn_ts_count(high_attn_ts_count = 3,
                                        ts_per_trial = 9,
                                        signal_dur = 3,
                                        p_obs_1_high_attn_sig_pres = 0.8, # h
                                        p_obs_1_high_attn_sig_abs = 0.2, # c
                                        ):
    
    accum_prob = 0
    # for any position of signal start
    for j in range(1, ts_per_trial+1):
        # for the 1st obs=1 to occur at any position within the signal duration
        for t_mu in range(j, j+signal_dur):
            # for the 1st obs=1 to occur at any order within the set of high-attention ts (given that all high-attention ts are within the bound of the n ts)
            for mu in range(max(1, high_attn_ts_count-(ts_per_trial-t_mu)), min(high_attn_ts_count, t_mu)+1): # we want to ensure that there's enough ts before the 1st obs=1, and enough ts after the 1st obs=1, to allow for m high-attention ts
                # for different numbers of high-attention ts within the signal duration before mu.
                for q in range(max(0, mu-j), min(t_mu-j, mu-1) +1):
                    # first calculate the probability that given t_mu, mu and q, to have (mu-1) high-attn ts before t_mu, in which we have (mu-1-q) ts before signal starts and q ts between signal starts and t_mu-1,
                    # as well as having (m-mu) high-attn ts after t_mu.
                    prob_combo = math.comb(j-1, mu-1-q) * math.comb(t_mu-j, q) * math.comb(ts_per_trial-t_mu, high_attn_ts_count-mu) / math.comb(ts_per_trial, high_attn_ts_count)
                    # then calculate the probability of the 1st obs=1 to occur at position t_mu
                    p_obs_1_at_t_mu = (1-p_obs_1_high_attn_sig_abs)**(mu-1-q) \
                                        *(1-p_obs_1_high_attn_sig_pres)**q \
                                        *p_obs_1_high_attn_sig_pres
                    combined_prob = prob_combo * p_obs_1_at_t_mu
                    accum_prob += combined_prob

                    # check if the total numbers are correct
                    if (mu-1-q) + (q) + (high_attn_ts_count-mu) + 1 != high_attn_ts_count:
                        raise ValueError('(mu-1-q) + (q) + (m-mu) + 1 != m')
                    if (j-1) + (t_mu-j) + (ts_per_trial-t_mu) + 1!= ts_per_trial:
                        raise ValueError('j-1 + t_mu-j + n-t_mu != n')
    accum_prob = accum_prob/ts_per_trial
    return accum_prob




def calc_prob_after_adding_to_existing_high_attn_ts(high_attn_ts=[],
                                 ts_per_trial = 9,
                                signal_dur = 3,
                                p_obs_1_high_attn_sig_pres = 0.8, # h
                                p_obs_1_high_attn_sig_abs = 0.2):

    possible_ts_to_add = [i for i in range(1, ts_per_trial+1) if i not in high_attn_ts]
    all_success_rates = []
    for new_ts in possible_ts_to_add:
        new_ts = [new_ts]
        new_success_rate = calc_prob_given_high_attn_ts_positions(high_attn_ts=high_attn_ts+new_ts, ts_per_trial=ts_per_trial, 
                                                                    signal_dur=signal_dur, p_obs_1_high_attn_sig_pres=p_obs_1_high_attn_sig_pres, 
                                                                    p_obs_1_high_attn_sig_abs=p_obs_1_high_attn_sig_abs)
        all_success_rates.append(new_success_rate)

    adding_ts_result_df = pd.DataFrame({'ts': possible_ts_to_add, 'success_rate': all_success_rates})
    adding_ts_result_df['ranking'] = adding_ts_result_df['success_rate'].rank(ascending=False, method='first')

    return adding_ts_result_df



    




