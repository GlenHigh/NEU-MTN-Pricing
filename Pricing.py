# -*- coding: utf-8 -*-
from typing import List
import numpy as np

from Rates import compute_discount_factors

class MonteCarloPricer(object):
    """ Monte Carlo pricer for our note
    """
    
    
    @staticmethod
    def generate_trajectories_bs(spot_init:float, dividend_yield:float,
                                 repo:float, volatility:float, risk_free:float,
                                 maturities:List[int], num_trajectories:int, 
                                 normal_matrix:np.ndarray=None):
        """ Generates the diffusion trajectories in Black & Scholes model
        """
        num_dates = len(maturities)
        if normal_matrix is None:
            normal_matrix = np.random.standard_normal(size=(num_dates - 1, num_trajectories))
            
        spot_trajectories = np.zeros(shape=(num_dates, num_trajectories))
        spot_trajectories[0,:] = np.ones(shape=(1, num_trajectories)) * spot_init
        delta_t = maturities[1:num_dates] - maturities[0:num_dates - 1]
        
        for t in range(num_dates - 1):
            spot_trajectories[t + 1,:] = np.multiply(spot_trajectories[t,:], 
                                                     np.exp((risk_free - repo - dividend_yield 
                                                            - 0.5 * pow(volatility, 2)) * delta_t[t]
                                                            + volatility * np.sqrt(delta_t[t])
                                                            * normal_matrix[t,:]))
        return np.transpose(spot_trajectories)
         
    @staticmethod



    @staticmethod
    def _compute_payoff(trajectory:np.ndarray, lock_in_level:float, barrier:float,
                       coupon_level:float, digi_coupon:float, risk_free:float) -> np.ndarray:
        """ Computes the discounted payoff for our note for a single simulated trajectory
        """
        cash_flows = np.zeros_like(trajectory)
        dfs = compute_discount_factors(risk_free, len(trajectory))
        
        max_perf = -1000
        for t in range(1, len(trajectory)):
            perf_t = trajectory[t] #/ trajectory[0]
            if perf_t > max_perf:
                max_perf = perf_t
                
            if max_perf >= lock_in_level:
                cash_flows[t:] += digi_coupon
                cash_flows[-1] += 1.00
                break
            
            if perf_t > coupon_level:
                cash_flows[t] += digi_coupon
            
            # Add redemption at maturity to cash flows
            if t == len(trajectory) - 1:
                if perf_t < barrier:
                    cash_flows[t] += perf_t
                else:
                    cash_flows[t] += 1.00
        
        discount_sum_cfs = np.sum(dfs * cash_flows)
        return np.sum(dfs * cash_flows)
    
    
    @staticmethod
    def price(all_simulations:np.ndarray, lock_in_level:float, barrier:float,
              coupon_level:float, digi_coupon:float, risk_free:float) -> float:
        """ Computes the mean payoff for all the simulations given for our Note.
        """
        num_simul = np.shape(all_simulations)[0]
        payoffs = np.zeros(num_simul)
        for simul in range(num_simul):
            payoffs[simul] = MonteCarloPricer._compute_payoff(all_simulations[simul,:], 
                                                              lock_in_level, barrier,
                                                              coupon_level, digi_coupon, 
                                                              risk_free)
        return np.mean(payoffs), np.std(payoffs)
    
    