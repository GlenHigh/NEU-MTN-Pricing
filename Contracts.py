# -*- coding: utf-8 -*-

class DownInPut(object):
    """ Down and out put
    """
    barrier:float = None
    
    def __init__(self, barrier:float):
        self.barrier = barrier
    

class LockInCall(object):
    """ Lock in call
    """
    lock_in_level:float = None
    
    def __init__(self, lock_in_level:float):
        self.lock_in_level = lock_in_level
        

class StructuredSEESGSEP(object):
    """ Lock In Binary Up Short DI put on SEESGSEP
    """
    maturity:int = None
    down_in_put:DownInPut = None
    lock_in_call:LockInCall = None
    notional:float = None
    digi_coupon:float = None
    coupon_level:float = None
    
    def __init__(self, maturity:int, notional:float, digi_coupon:float, 
                 coupon_level:float, down_in_put:DownInPut, lock_in_call:LockInCall):
        self.down_in_put = down_in_put
        self.lock_in_call = lock_in_call
        self.maturity = maturity
        self.notional = notional
        self.digi_coupon = digi_coupon
        self.coupon_level = coupon_level


class StructuredSEESGSEPBuilder(object):
    """ Static builder pattern class for StructuredSEESGSEP
    """
    
    @staticmethod
    def build(maturity:int, notional:float, digi_coupon:float, coupon_level:float, 
              lock_in_level:float, barrier:float) -> StructuredSEESGSEP:
        put = DownInPut(barrier)
        call = LockInCall(lock_in_level)
        return StructuredSEESGSEP(maturity, notional, digi_coupon, coupon_level, put, call)
        