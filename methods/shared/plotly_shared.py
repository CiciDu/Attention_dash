from methods.plot_methods import plt_simulation
from methods.shared import plt_shared
import plotly.graph_objects as go
import plotly.express as px
import numpy as np




def add_to_base_plot(fig, x, y, ts_to_plot, ts_per_trial, rank_to_start, rank_to_end):
    fig = add_high_attention_points(fig, x, y, ts_to_plot)
    label_dict = plt_shared.generate_label_dict()
    fig = add_labels_and_title(fig, x, y, label_dict, rank_to_start, rank_to_end, ts_per_trial)
    if y=='ranking':
        fig = label_with_success_rate(fig, ts_per_trial, ts_to_plot)
    fig = update_axis(fig, y, ts_to_plot, rank_to_end)
    return fig 



def add_high_attention_points(fig, x, y, ts_to_plot):
    high_attention_points = ts_to_plot[ts_to_plot['attn_ts_counter'] >= 0]
    fig.add_trace(go.Scatter(x=high_attention_points[x], y=high_attention_points[y], mode='markers', 
                             marker=dict(size=14, color='black', symbol='circle-open'), name='High attention time steps',
                             hovertemplate=None, hoverinfo='none'))
    # move the legend to the top
    fig.update_layout(legend=dict(yanchor="top", y=1.05, xanchor="left", x=0.01))

    return fig


def add_dashed_horizontal_lines(fig, y, ts_per_trial, ts_to_plot):
    for y_value in ts_to_plot[y].unique():
        fig.add_shape(type="line", x0=1, y0=y_value, x1=ts_per_trial, y1=y_value, line=dict(color="grey", width=1, dash="dash"))
    return fig


def label_with_success_rate(fig, ts_per_trial, ts_to_plot):
    ts_to_plot = ts_to_plot[['ranking', 'success_rate']].copy()
    # since only the ranking is shown, label each horizontal line with the success rate
    for i in range(ts_to_plot.shape[0]):
        fig.add_annotation(x=ts_per_trial+0.7, y=ts_to_plot.iloc[i]['ranking'], text=str(round(ts_to_plot.iloc[i]['success_rate'], 3)), showarrow=False)
    fig.add_annotation(x=ts_per_trial+0.7, y=ts_to_plot['ranking'].min()-1, text='Success rate', showarrow=False)
    # if rank_to_end == 'lowest':
    #     fig.add_annotation(x=ts_per_trial+0.7, y=ts_to_plot['ranking'].max()+1, text='Success rate', showarrow=False)
    # else:
    #     fig.add_annotation(x=ts_per_trial+0.7, y=ts_to_plot['ranking'].min()-1, text='Success rate', showarrow=False)
    return fig



def add_labels_and_title(fig, x, y, label_dict, rank_to_start, rank_to_end, ts_per_trial):
    fig.update_layout(#title='Top {} high-attention timestep combinations'.format(rank_to_start) if rank_to_end == 'highest' else 'Bottom {} high-attention timestep combinations'.format(rank_to_start), 
                      title = f'High-attention timestep combinations: rank {rank_to_start} to {rank_to_end}', 
                      title_x=0.5,
                      xaxis_title=label_dict[x], 
                      yaxis_title=label_dict[y], 
                      coloraxis=dict(colorscale='Viridis'))
    fig.update_xaxes(tickvals=np.arange(1, ts_per_trial+1))
    
    return fig



def update_axis(fig, y, ts_to_plot, rank_to_end):
    if y=='success_rate':
        # make the colors more transparent.
        fig.update_traces(marker=dict(opacity=0.5))
    elif y=='ranking':
        fig.update_yaxes(tickvals=np.arange(min(ts_to_plot['ranking']), max(ts_to_plot['ranking'])+1))
        #if rank_to_end == 'highest':
        fig.update_yaxes(autorange="reversed")
    return fig




def label_colorbar(fig, hue_label):
    fig.update_layout(coloraxis_colorbar=dict(title=hue_label))
    # make the colorbar title vertical
    fig.update_layout(coloraxis_colorbar=dict(title_side="right"))
    return fig
