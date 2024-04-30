from methods.simulation_methods import simulation_func, find_info_for_ts, find_info_for_combo
import numpy as np
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import random
import plotly.graph_objects as go


def determine_variable_for_hue(hue_var, hue_denominator, hue_numerator, label_dict, ts_to_plot):
    if hue_var is not None:
        hue_values = ts_to_plot[hue_var]
    else:
        if (hue_numerator is None) or (hue_denominator is None):
            raise ValueError('If hue_var is None, then hue_numerator and hue_denominator must be provided')
        hue_values = ts_to_plot[hue_numerator] / ts_to_plot[hue_denominator]
    hue_label = generate_hue_label(label_dict, hue_var=hue_var, denominator=hue_denominator, numerator=hue_numerator)
    return hue_values, hue_label


def generate_hue_label(label_dict, hue_var, denominator, numerator):
    if hue_var is not None:
        hue_label = label_dict[hue_var]
    else:
        hue_label = '{} / \n {}'.format(label_dict[numerator], label_dict[denominator])
    return hue_label


def create_base_plot(x, y, hue_values, ts_to_plot):
    # plot a filled circle for each time step for each combo_id, with color indicating the percentage of trials with observation 1
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.yaxis.grid(False) # Hide the horizontal gridlines
    sns.scatterplot(ts_to_plot, x=x, y=y, marker='o', s=100, hue=hue_values, palette='viridis', legend=False, ax=ax)
    sns.set_theme(style="whitegrid")
    return fig, ax


def add_high_attention_points(ax, x, y, ts_to_plot):
    # plot a black hollow circle for high attention time steps for each combo_id
    sns.scatterplot(ts_to_plot[ts_to_plot['attn_ts_counter'] >= 0], x=x, y=y, marker='o', s=140, facecolor="none", edgecolor='black', linewidth=1.5, legend=False, ax=ax)
    return ax

def add_dashed_horizontal_lines(ax, y, ts_per_trial, combo_id_df_to_plot):
    # draw a dashed horizontal line for each value of success rate
    for i in range(combo_id_df_to_plot.shape[0]):
        ax.hlines(combo_id_df_to_plot[y].iloc[i], 0, ts_per_trial-1, linestyles='dashed', colors='grey', alpha=0.3)
    return ax

def label_with_success_rate(ax, y, ts_per_trial, combo_id_df_to_plot, highest_or_lowest):
    # since only the ranking is shown, label each horizontal line with the success rate
    for i in range(combo_id_df_to_plot.shape[0]):
        ax.text(ts_per_trial+0.3, combo_id_df_to_plot[y].iloc[i], 
                str(round(combo_id_df_to_plot['combo_success_rate'].iloc[i], 2)), 
                color='black', fontsize=10, ha='left', va='center')
    # label the above as success rate, with the position taking into consideration whether the ax is inverted
    if highest_or_lowest == 'lowest':
        ax.text(ts_per_trial, combo_id_df_to_plot[y].max()+0.5, 'Success rate', color='black', fontsize=12, ha='left', va='center')
    else:
        ax.text(ts_per_trial, combo_id_df_to_plot[y].min()-0.5, 'Success rate', color='black', fontsize=12, ha='left', va='center')
    return ax



def add_labels_and_title(ax, x, y, label_dict, n_combo_to_plot, highest_or_lowest):
    ax.set_xlabel(label_dict[x])
    ax.set_ylabel(label_dict[y])
    if highest_or_lowest == 'highest':
        ax.set_title('Top {} high-attention timestep combinations'.format(n_combo_to_plot), fontsize=15)
        ax.invert_yaxis()
    else:
        ax.set_title('Bottom {} high-attention timestep combinations'.format(n_combo_to_plot), fontsize=15)
    return ax

def add_colorbar(ax, hue_label):
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    plt.colorbar(sm, ticks=[0, 0.5, 1], cax=ax.figure.add_axes([0.98, 0.1, 0.03, 0.8]), orientation='vertical').set_label(label=hue_label, size=15)
    return ax



def generate_label_dict():
    label_dict = {'ts': 'Time step', 
                    'n_trial_ts_obs_1_any_order': '# trials where ts has obs=1 at any order',
                    'n_trial_ts_obs_1_first': '# trials where ts first has obs=1',
                    'n_rewarded_trial_ts_obs_1_any_order': '# rewarded trials where ts has obs=1 at any order',
                    'n_rewarded_trial_ts_obs_1_first': '# rewarded trials where ts first has obs=1',
                    'n_rewarded_trial_for_combo': '# rewarded trials for the high-attention ts combo',
                    'combo_id': 'Combo ID',
                    'combo_num_trial': '# trials simulated for each combo',
                    'combo_success_rate': 'Success rate for the high-attention ts combo',
                    'success_rate_ranking': 'Ranking of the success rate',
                    'attn_ts_counter': 'Attention time step counter',
                    'perc_trial_ts_obs_1_any_order': '% trials where ts has obs=1 at any order',
                    'perc_trial_ts_obs_1_first': '% trials where ts first has obs=1',
                    'perc_rewarded_trial_ts_obs_1_any_order': '% trials rewarded where ts has obs=1 at any order',
                    'perc_rewarded_trial_ts_obs_1_first': '% trials rewarded where ts first has obs=1',
                    'ratio_of_ts_obs_1_first_OVER_ts_obs_1_any_order': 'Ratio of ts obs=1 first over ts obs=1 any order'}
    return label_dict
    

def plt_simulation_results(x='ts', y='combo_success_rate', hue_var=None, hue_denominator='n_trial_ts_obs_1_first', hue_numerator='n_rewarded_trial_ts_obs_1_first', 
                            ts_to_plot=None, combo_id_df_to_plot=None, ts_per_trial=None, n_combo_to_plot=None, highest_or_lowest=None, show_plot=True):
    hue_values, hue_label = determine_variable_for_hue(hue_var, hue_denominator, hue_numerator, label_dict, ts_to_plot)
    fig, ax = create_base_plot(x, y, hue_values, ts_to_plot)
    ax = add_high_attention_points(ax, x, y, ts_to_plot)
    ax = add_dashed_horizontal_lines(ax, y, ts_per_trial, combo_id_df_to_plot)
    if y == 'success_rate_ranking':
        ax = label_with_success_rate(ax, y, ts_per_trial, combo_id_df_to_plot, highest_or_lowest)
    label_dict = generate_label_dict()
    ax = add_labels_and_title(ax, x, y, label_dict, n_combo_to_plot, highest_or_lowest)
    ax = add_colorbar(ax, hue_label)
    if show_plot:
        plt.show()
    return fig, ax



