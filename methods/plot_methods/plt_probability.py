import numpy as np
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
from numpy import random
import plotly.graph_objects as go


import matplotlib.pyplot as plt

def plot_success_rate_after_adding_to_high_attn_ts(adding_ts_df, high_attn_ts, show_plot=True):
    # make a bar plot for the success rates
    fig, ax = plt.subplots()

    # Change the bar color and edge color
    ax.bar(adding_ts_df['ts'], adding_ts_df['success_rate'], color='skyblue', edgecolor='black')

    # Set the title and labels with custom font sizes
    ax.set_xlabel("New high attention time step", fontsize=12)
    ax.set_ylabel("New probability of success", fontsize=12)
    ax.set_title("New success rate by adding to existing high attention time steps: " + ', '.join(map(str, high_attn_ts)), fontsize=14, pad=30)  # Add padding to the title
    plt.subplots_adjust(top=0.9) 

    # make the x tick labels span all integers in the range
    ax.set_xticks(np.arange(1, max(adding_ts_df['ts'])+1))

    # Change the background color of the plot
    ax.set_facecolor('white')

    # Change the grid color and line style
    ax.grid(color='gray', linestyle='--', linewidth=0.5)

    if show_plot:
        plt.show()

    return fig, ax