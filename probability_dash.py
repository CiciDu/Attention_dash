from methods.dash_methods import dash_probability_class


if __name__ == '__main__':
    dp = dash_probability_class.DashProbability()
    dp.calculate_probability()
    dp.plot_probability_in_plotly(show_plot=False)
    dp.make_dash_for_main_plots()
    server = dp.app.server
    dp.app.run_server(port=8052)
