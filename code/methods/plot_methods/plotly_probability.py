import plotly.graph_objects as go
import plotly.express as px
import numpy as np

def plot_success_rate_after_adding_to_high_attn_ts(adding_ts_df, high_attn_ts, show_plot=True):
    # make a bar plot for the success rates
    
    fig=px.bar(adding_ts_df, x='ts',y='success_rate',
            color = 'success_rate_ranking',
            color_continuous_scale='Viridis_r',
            labels={'ts':'New high attention time step', 
                    'success_rate':'New success rate',
                    'success_rate_ranking':'Success Rate Ranking'},
            title="New success rate by adding to existing high attention time steps: " + ', '.join(map(str, high_attn_ts)),
            hover_data={'ts':False, 'success_rate':True, 'success_rate_ranking':False},
            hover_name='success_rate_ranking',
            text='success_rate_ranking',
            )
 

    # make x tick labels integers
    fig.update_xaxes(tickvals=np.arange(1, max(adding_ts_df['ts'])+1))

    # make the hover text show only 3 decimals. Make it percentage
    fig.update_traces(hovertemplate='Success Rate: %{y:.3f}')


    # change the label of the colorbar
    ranking=['1st', '2nd', '3rd', '4th', '5th', '6th', '7th', '8th', '9th', '10th',
                '11th', '12th', '13th', '14th', '15th', '16th', '17th', '18th', '19th', '20th']
    if len(adding_ts_df) <= 20:
        ranking = ranking[:len(adding_ts_df)]
    else:
        ranking = np.arange(1, len(adding_ts_df)+1).tolist()
    fig.update_coloraxes(colorbar=dict(
        tickvals=np.arange(1, len(adding_ts_df)+1),
        ticktext=ranking,
    ))



    if show_plot:
        fig.show()

    return fig