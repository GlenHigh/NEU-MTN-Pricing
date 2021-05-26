# -*- coding: utf-8 -*-
from typing import List

import numpy as np

from Pricing import MonteCarloPricer


class GreekComputer(object):
    """ Computes greeks for our Note
    """
    
    _step_spot = 1
    spot = np.linspace(1,200,200 * _step_spot)
    _step_gamma = 5
    _step_vol = 0.01
    
    @staticmethod
    def compute_prices_for_delta_bs(dividend_yield:float, repo_rate:float,
                                   volatility:float, risk_free_rate:float,
                                   dates:List[int], num_trajectories:int,
                                   strike:float, lock_in_level:float, 
                                   barrier:float, coupon_level:float,
                                   digi_coupon:float) -> (List[float], List[float]):
        """ 
        Computes the product prices necessary for delta analysis
        """
        prices_for_delta = np.zeros_like(GreekComputer.spot)
        errors = np.zeros_like(GreekComputer.spot)
        normal_matrix = np.random.standard_normal(size=(len(dates) - 1, num_trajectories))
        for i in range(len(GreekComputer.spot)):
            spot_init = GreekComputer.spot[i]
            spot_trajectories = MonteCarloPricer.generate_trajectories_bs(spot_init, dividend_yield, 
                                                                          repo_rate, volatility, risk_free_rate, 
                                                                          dates, num_trajectories, normal_matrix)
            normalized_spot = spot_trajectories / strike
            prices_for_delta[i], errors[i] = MonteCarloPricer.price(normalized_spot, lock_in_level, barrier, 
                                                                    coupon_level, digi_coupon, risk_free_rate)
        return prices_for_delta, errors
    
    
    @staticmethod
    def compute_delta(prices_for_delta:List[float], strike:float) -> List[float]:
        """
        Computes product delta as function of spot
        """
        return (prices_for_delta[1:] - prices_for_delta[:-1]) / strike
    
    
    @staticmethod
    def compute_gamma(prices_for_delta:List[float]) -> List[float]:
        """
        Computes product gamma as function of spot
        """
        return (prices_for_delta[2 * GreekComputer._step_gamma:] + prices_for_delta[:-2 * GreekComputer._step_gamma] 
                - 2 * prices_for_delta[GreekComputer._step_gamma:-GreekComputer._step_gamma]) \
                / pow(GreekComputer._step_spot * GreekComputer._step_gamma, 2)
    
    
    @staticmethod
    def compute_prices_for_vega_bs(volatility:float, dividend_yield:float, repo_rate:float,
                                   risk_free_rate:float, dates:List[int], num_trajectories:int,
                                   strike:float, lock_in_level:float, barrier:float, 
                                   coupon_level:float, digi_coupon:float) -> (List[float], List[float]):
        """
        Computes product prices necessary for analysis of vega
        """
        vol = [volatility - 0.5 * GreekComputer._step_vol, volatility + 0.5 * GreekComputer._step_vol]
        prices_for_vega = np.zeros(shape=(len(vol), len(GreekComputer.spot)))
        errors = np.zeros_like(prices_for_vega)
        
        normal_matrix = np.random.standard_normal(size=(len(dates) - 1, num_trajectories))
        for i in range(len(GreekComputer.spot)):
            for j in range(len(vol)):
                spot_init = GreekComputer.spot[i]
                vol_init = vol[j]
                spot_trajectories = MonteCarloPricer.generate_trajectories_bs(spot_init, dividend_yield,
                                                                              repo_rate, vol_init, risk_free_rate,
                                                                              dates, num_trajectories, normal_matrix)
                normalized_spot = spot_trajectories / strike
                prices_for_vega[j, i], errors[j, i] = MonteCarloPricer.price(normalized_spot, lock_in_level, barrier, 
                                                                             coupon_level, digi_coupon, risk_free_rate)
        return prices_for_vega, errors
    
        
    @staticmethod
    def compute_vega(prices_for_vega:List[float]) -> List[float]:
        """
        Computes product vega as function of spot
        """
        return prices_for_vega[1,:] - prices_for_vega[0,:]