from methods.dash_methods import dash_cond_probability_class

cp = dash_cond_probability_class.DashCondProbability()
cp.calculate_probability()
cp.plot_probability_in_plotly(show_plot=False)
cp.make_dash_for_main_plots()

server = cp.app.server

if __name__ == '__main__':
    cp.app.run_server(port=8054)
