from methods.dash_methods import dash_probability_class

dp = dash_probability_class.DashProbability()
dp.prepare_to_use_dash()
dp.make_dash_for_main_plots()
server = dp.app.server

if __name__ == '__main__':
    dp.app.run_server(port=8053)
