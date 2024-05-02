from enum import unique
from methods.plot_methods import plt_simulation
import numpy as np
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import random
import plotly.graph_objects as go
import matplotlib.pyplot as plt


def add_to_base_plot(ax, x, y, ts_to_plot, ts_per_trial, n_combo_to_plot, highest_or_lowest):
    ax = add_high_attention_points(ax, x, y, ts_to_plot)
    ax = add_dashed_horizontal_lines(ax, y, ts_per_trial, ts_to_plot)
    ax = update_axis(ax, y, ts_to_plot, ts_per_trial)
    label_dict = generate_label_dict()
    ax = add_labels_and_title(ax, x, y, label_dict, n_combo_to_plot, highest_or_lowest)
    if y == 'ranking':
        ax = label_with_success_rate(ax, ts_per_trial, ts_to_plot, highest_or_lowest)
    return ax


def update_axis(ax, y, ts_to_plot, ts_per_trial):
    ax.yaxis.grid(False) # Hide the horizontal gridlines
    ax.set_axisbelow(True)
    sns.set_theme(style="whitegrid")
    ax.set_xticks(np.arange(1, ts_per_trial+1))
    ax.set_yticks(np.arange(ts_to_plot[y].min(), ts_to_plot[y].max()+1))
    return ax


def add_high_attention_points(ax, x, y, ts_to_plot):
    # plot a black hollow circle for high attention time steps for each combo_id
    sns.scatterplot(ts_to_plot[ts_to_plot['attn_ts_counter'] >= 0], x=x, y=y, marker='o', s=140, facecolor="none", edgecolor='black', linewidth=1.5, legend=False, ax=ax)
    return ax

def add_dashed_horizontal_lines(ax, y, ts_per_trial, ts_to_plot):
    # draw a dashed horizontal line for each value of success rate
    for y_value in np.unique(ts_to_plot[y].values):
        ax.hlines(y_value, 1, ts_per_trial, linestyles='dashed', colors='grey', alpha=0.3)
    return ax

def label_with_success_rate(ax, ts_per_trial, ts_to_plot, highest_or_lowest):
    ts_to_plot = ts_to_plot.copy()
    ts_to_plot = ts_to_plot[['ranking', 'success_rate']].drop_duplicates()
    for i in range(ts_to_plot.shape[0]):
    # since only the ranking is shown, label each horizontal line with the success rate
        ax.text(ts_per_trial+0.3, ts_to_plot.iloc[i]['ranking'], 
                str(round(ts_to_plot.iloc[i]['success_rate'], 3)), 
                color='black', fontsize=10, ha='left', va='center')
    # label the above as success rate, with the position taking into consideration whether the ax is inverted
    if highest_or_lowest == 'lowest':
        ax.text(ts_per_trial, ts_to_plot['ranking'].max()+0.5, 'Success rate', color='black', fontsize=12, ha='left', va='center')
    else:
        ax.text(ts_per_trial, ts_to_plot['ranking'].min()-0.5, 'Success rate', color='black', fontsize=12, ha='left', va='center')
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


def generate_label_dict():
    label_dict = {'ts': 'Time step', 
                    'n_trial_ts_obs_1_any_order': '# trials where ts has obs=1 at any order',
                    'n_trial_ts_obs_1_first': '# trials where ts first has obs=1',
                    'n_rewarded_trial_ts_obs_1_any_order': '# rewarded trials where ts has obs=1 at any order',
                    'n_rewarded_trial_ts_obs_1_first': '# rewarded trials where ts first has obs=1',
                    'n_rewarded_trial_for_combo': '# rewarded trials for the high-attention ts combo',
                    'combo_id': 'Combo ID',
                    'combo_num_trial': '# trials simulated for each combo',
                    'success_rate': 'Success rate for the high-attention ts combo',
                    'ranking': 'Ranking of the success rate',
                    'attn_ts_counter': 'Attention time step counter',
                    'perc_trial_ts_obs_1_any_order': '% trials where ts has obs=1 at any order',
                    'perc_trial_ts_obs_1_first': '% trials where ts first has obs=1',
                    'perc_rewarded_trial_ts_obs_1_any_order': '% trials rewarded where ts has obs=1 at any order',
                    'perc_rewarded_trial_ts_obs_1_first': '% trials rewarded where ts first has obs=1',
                    'ratio_of_ts_obs_1_first_OVER_ts_obs_1_any_order': 'Ratio of ts obs=1 first over ts obs=1 any order'}
    return label_dict