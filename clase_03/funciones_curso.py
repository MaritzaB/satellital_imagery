# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:49:56 2023

@author: Dr. Frank Olaya, Baja Marine Science A.C.
"""

def timeDatetime64(time1):
    import pandas as pd
    dates=pd.DatetimeIndex(time1)
    # dates.year
    # dates.month
    # dates.day
    yyyy=[x.year for x in dates.tolist()]
    mm=[x.month for x in dates.tolist()]
    dd=[x.day for x in dates.tolist()]
    return yyyy,mm,dd