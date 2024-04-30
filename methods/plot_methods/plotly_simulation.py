from methods.plot_methods import plt_simulation
import plotly.graph_objects as go
import plotly.express as px





def create_base_plot(x, y, hue_values, hue_label, label_dict, ts_to_plot, color_scale='viridis', tick_mode='array'):
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
                     custom_data=['hue_values', 'high_attn_ts_combo', 'combo_success_rate', 'success_rate_ranking'],
                     hover_name=y)

    if y=='combo_success_rate':
        # make the colors more transparent.
        fig.update_traces(marker=dict(opacity=0.5))

    hovertemplate = 'Ranking of success rate: %{customdata[3]}<br>' + \
                    'Success rate: %{customdata[2]}<br>' + \
                    hue_label + ': %{customdata[0]:.2f}<br>' +\
                    'high attention time steps: %{customdata[1]}'

    fig.update_traces(hovertemplate=hovertemplate, showlegend=False)
    #fig.update_layout(hovermode="y unified")

    fig.update_xaxes(tickmode=tick_mode, tickvals=[i for i in range(int(ts_to_plot[x].min()), int(ts_to_plot[x].max())+1)])
    if y=='success_rate_ranking':
        fig.update_yaxes(tickmode=tick_mode, tickvals=[i for i in range(int(ts_to_plot[y].min()), int(ts_to_plot[y].max())+1)])
    
    return fig



def add_high_attention_points(fig, x, y, ts_to_plot):
    high_attention_points = ts_to_plot[ts_to_plot['attn_ts_counter'] >= 0]
    fig.add_trace(go.Scatter(x=high_attention_points[x], y=high_attention_points[y], mode='markers', 
                             marker=dict(size=14, color='black', symbol='circle-open'), name='High attention time steps',
                             hovertemplate=None, hoverinfo='none'))
    # move the legend to the top
    fig.update_layout(legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.01))
    return fig


def add_dashed_horizontal_lines(fig, y, ts_per_trial, combo_id_df_to_plot):
    for i in range(combo_id_df_to_plot.shape[0]):
        fig.add_shape(type="line", x0=0, y0=combo_id_df_to_plot[y].iloc[i], x1=ts_per_trial-1, y1=combo_id_df_to_plot[y].iloc[i], line=dict(color="grey", width=1, dash="dash"))
    return fig


def label_with_success_rate(fig, y, ts_per_trial, combo_id_df_to_plot, highest_or_lowest):
    for i in range(combo_id_df_to_plot.shape[0]):
        fig.add_annotation(x=ts_per_trial+0.7, y=combo_id_df_to_plot[y].iloc[i], text=str(round(combo_id_df_to_plot['combo_success_rate'].iloc[i], 2)), showarrow=False)
    if highest_or_lowest == 'lowest':
        fig.add_annotation(x=ts_per_trial+0.7, y=combo_id_df_to_plot[y].max()+0.5, text='Success rate', showarrow=False)
    else:
        fig.add_annotation(x=ts_per_trial+0.7, y=combo_id_df_to_plot[y].min()-0.5, text='Success rate', showarrow=False)
    return fig

def add_labels_and_title(fig, x, y, label_dict, n_combo_to_plot, highest_or_lowest):
    fig.update_layout(title='Top {} high-attention timestep combinations'.format(n_combo_to_plot) if highest_or_lowest == 'highest' else 'Bottom {} high-attention timestep combinations'.format(n_combo_to_plot), xaxis_title=label_dict[x], yaxis_title=label_dict[y], title_x=0.5)
    if (highest_or_lowest == 'highest') & (y == 'success_rate_ranking'):
        # invert y axis
        fig.update_yaxes(autorange="reversed")
    return fig


def label_colorbar(fig, hue_label):
    fig.update_layout(coloraxis_colorbar=dict(title=hue_label))
    # make the colorbar title vertical
    fig.update_layout(coloraxis_colorbar=dict(title_side="right"))
    return fig


def plt_simulation_results(x='ts', y='combo_success_rate', hue_var=None, hue_denominator='n_trial_ts_obs_1_first', hue_numerator='n_rewarded_trial_ts_obs_1_first', 
                            ts_to_plot=None, combo_id_df_to_plot=None, ts_per_trial=None, n_combo_to_plot=None, highest_or_lowest=None, show_plot=True):
    label_dict = plt_simulation.generate_label_dict()
    hue_values, hue_label = plt_simulation.determine_variable_for_hue(hue_var, hue_denominator, hue_numerator, label_dict, ts_to_plot)
    fig = create_base_plot(x, y, hue_values,  hue_label, label_dict, ts_to_plot)
    fig = add_high_attention_points(fig, x, y, ts_to_plot)
    #fig = add_dashed_horizontal_lines(fig, y, ts_per_trial, combo_id_df_to_plot)
    if y == 'success_rate_ranking':
        fig = label_with_success_rate(fig, y, ts_per_trial, combo_id_df_to_plot, highest_or_lowest)
    fig = add_labels_and_title(fig, x, y, label_dict, n_combo_to_plot, highest_or_lowest)
    fig = label_colorbar(fig, hue_label)
    if show_plot:
        fig.show()
    return fig