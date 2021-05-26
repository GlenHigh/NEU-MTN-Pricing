# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
#import matplotlib.pyplot as plt

#plt.style.use("seaborn")

from Pricing import MonteCarloPricer
from RiskEngine import GreekComputer

# Estimate underlying characteristics for diffusion simulations
data = pd.read_excel("../data/seesgsep_index.xlsx", skiprows=6)
spot = data["PX_LAST"]
volatility = np.std(spot.values) / 100


# Establish contract characteristics
maturity = 8
frequency = 1
dates = np.linspace(1, maturity, num=maturity * frequency)
lock_in_level = 1.20
barrier = 0.60
notional = 150000
digi_coupon = 0.053
coupon_level = 1.00
strike = 100

# Establish market characteristics
dividend_yield = 0.02
repo_rate = 0.01
risk_free_rate = 0.01
spot_init = 100

# Establish simulation parameters 
NUM_SIMUL = 10000

normal_matrix = np.random.standard_normal(size=(len(dates) - 1, NUM_SIMUL))
trajectories = MonteCarloPricer.generate_trajectories_bs(spot_init, dividend_yield, repo_rate, 
                                                         volatility, risk_free_rate, dates, NUM_SIMUL, normal_matrix)
trajectories /= 100.00
price, error = MonteCarloPricer.price(trajectories, lock_in_level, barrier, coupon_level, digi_coupon, 
                                      risk_free_rate)


# DELTA BS
prices_for_delta_bs, errors_delta_bs = GreekComputer.compute_prices_for_delta_bs(dividend_yield, repo_rate,
                                                                                 volatility, risk_free_rate, 
                                                                                 dates, NUM_SIMUL, strike, 
                                                                                 lock_in_level, barrier, 
                                                                                 coupon_level, digi_coupon)

delta_bs = GreekComputer.compute_delta(prices_for_delta_bs, strike)

fig, ax = plt.subplots(1)
ax.scatter(GreekComputer.spot[1:], delta_bs, color="maroon")
plt.title("Note Delta")
plt.savefig("figures/note_delta.png");

# GAMMA BS 
gamma_bs = GreekComputer.compute_gamma(prices_for_delta_bs)

fig, ax = plt.subplots(1)
ax.scatter(GreekComputer.spot[GreekComputer._step_gamma:-GreekComputer._step_gamma], 
        gamma_bs, color="maroon")
plt.title("Note Gamma")
plt.savefig("figures/note_gamma.png");

# VEGA BS
prices_for_vega_bs, errors_vega_bs = GreekComputer.compute_prices_for_vega_bs(volatility, dividend_yield, repo_rate, 
                                                                              risk_free_rate, dates, NUM_SIMUL, 
                                                                              strike, lock_in_level, barrier, 
                                                                              coupon_level, digi_coupon)
vega_bs = GreekComputer.compute_vega(prices_for_vega_bs)



