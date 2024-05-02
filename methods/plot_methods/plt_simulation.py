from methods.simulation_methods import simulation_func, find_info_for_ts, find_info_for_combo
from methods.plot_methods import plt_shared
import numpy as np
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import random
import plotly.graph_objects as go


    

def plot_simulation_results(x='ts', y='ranking', hue_var=None, hue_denominator='n_trial_ts_obs_1_first', hue_numerator='n_rewarded_trial_ts_obs_1_first', 
                            ts_to_plot=None, ts_per_trial=None, n_combo_to_plot=None, highest_or_lowest=None, show_plot=True):
    label_dict = plt_shared.generate_label_dict()
    hue_values, hue_label = determine_variable_for_hue(hue_var, hue_denominator, hue_numerator, label_dict, ts_to_plot)
    fig, ax = create_base_plot(x, y, hue_values, ts_to_plot)
    ax = plt_shared.add_to_base_plot(ax, x, y, ts_to_plot, ts_per_trial, n_combo_to_plot, highest_or_lowest)
    ax = plt_shared.add_dashed_horizontal_lines(ax, y, ts_per_trial, ts_to_plot)
    ax = add_colorbar(ax, hue_label)
    if show_plot:
        plt.show()
    return fig, ax


def create_base_plot(x, y, hue_values, ts_to_plot):
    # plot a filled circle for each time step for each combo_id, with color indicating the percentage of trials with observation 1
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.scatterplot(ts_to_plot, x=x, y=y, marker='o', s=70, hue=hue_values, palette='viridis', legend=False, ax=ax)
    return fig, ax



def determine_variable_for_hue(hue_var, hue_denominator, hue_numerator, label_dict, ts_to_plot):
    if hue_var is not None:
        hue_values = ts_to_plot[hue_var]
    else:
        if (hue_numerator is None) or (hue_denominator is None):
            raise ValueError('If hue_var is None, then hue_numerator and hue_denominator must be provided')
        hue_values = ts_to_plot[hue_numerator] / ts_to_plot[hue_denominator]
    # replace na in hue_values with 0
    hue_values.fillna(0, inplace=True)
    hue_label = generate_hue_label(label_dict, hue_var=hue_var, denominator=hue_denominator, numerator=hue_numerator)
    return hue_values, hue_label


def generate_hue_label(label_dict, hue_var, denominator, numerator):
    if hue_var is not None:
        hue_label = label_dict[hue_var]
    else:
        hue_label = '{} / \n {}'.format(label_dict[numerator], label_dict[denominator])
    return hue_label



def add_colorbar(ax, hue_label):
    sm = plt.cm.ScalarMappable(cmap='viridis', norm=plt.Normalize(vmin=0, vmax=1))
    sm.set_array([])
    plt.colorbar(sm, ticks=[0, 0.5, 1], cax=ax.figure.add_axes([0.98, 0.1, 0.03, 0.8]), orientation='vertical').set_label(label=hue_label, size=15)
    return ax





