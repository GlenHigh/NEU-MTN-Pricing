# -*- coding: utf-8 -*-
import numpy as np

def compute_discount_factors(risk_free_rate:float, last_date:int):
    """ 
    Computes all the discount factors until the last date given
    """
    return np.exp(-risk_free_rate * np.linspace(1, last_date, last_date))
