from methods.plot_methods import plt_simulation
from methods.shared import plotly_shared, plt_shared
import plotly.graph_objects as go
import plotly.express as px



def plot_simulation_results_in_plotly(x='ts', y='ranking', hue_var=None, hue_denominator='n_trial_ts_obs_1_first', hue_numerator='n_rewarded_trial_ts_obs_1_first', 
                            ts_to_plot=None, ts_per_trial=None, rank_to_start=None, rank_to_end=15, show_plot=True):
    label_dict = plt_shared.generate_label_dict()
    hue_values, hue_label = plt_simulation.determine_variable_for_hue(hue_var, hue_denominator, hue_numerator, label_dict, ts_to_plot)
    
    fig = create_base_plot(x, y, hue_values,  hue_label, ts_to_plot)
    fig = plotly_shared.add_to_base_plot(fig, x, y, ts_to_plot, ts_per_trial, rank_to_start, rank_to_end)
    fig = plotly_shared.label_colorbar(fig, hue_label)

    if show_plot:
        fig.show()
    return fig


def create_base_plot(x, y, hue_values, hue_label, ts_to_plot, color_scale='viridis'):
    """
    Create a scatter plot with Plotly Express and customize the hover data.

    Parameters:
    x (str): The column name to be used for the x-axis.
    y (str): The column name to be used for the y-axis.
    hue_values (Series or list): The values to be used for the color scale.
    hue_label (str): The label for the hue_values in the hover data.
    label_dict (dict): A dictionary mapping column names to labels.
    ts_to_plot (DataFrame): The DataFrame containing the data to be plotted.
    color_scale (str): The color scale to be used for the hue_values. Default is 'viridis'.
    tick_mode (str): The tick mode to be used for the x and y axes. Default is 'array'.
    """
    ts_to_plot = ts_to_plot.copy()
    ts_to_plot['hue_values'] = hue_values

    fig = px.scatter(ts_to_plot, x=x, y=y, color='hue_values', color_continuous_scale=color_scale, 
                     custom_data=['high_attn_ts_combo', 'success_rate', 'ranking', 'hue_values'],
                     hover_name=y)


    hovertemplate = 'Ranking of success rate: %{customdata[2]}<br>' + \
                    'Success rate: %{customdata[1]:.4f}<br>' + \
                    hue_label + ': %{customdata[3]:.2f}<br>' +\
                    'high attention time steps: %{customdata[0]}'

    fig.update_traces(hovertemplate=hovertemplate, showlegend=False)

    num_rows = len(ts_to_plot[y].unique())
    fig.update_layout(height=max(500, 300 + 25 * num_rows))


    return fig

