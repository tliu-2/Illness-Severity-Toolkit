import pandas as pd
import math

def get_age_score(age):
    if math.isnan(age):
        return math.nan

    if age < 50:
        return 0
    elif age >= 50:
        if age < 60:
            return 1
        elif age >= 60:
            if age < 70:
                return 2
            elif age >= 70:
                if age < 80:
                    return 3
                else: # age >= 80
                    return 4


def weight1(x):
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 1
    else: # x == 0
        return 0

def weight2(x):
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 2
    else:
        return 0

def weight3(x):
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 3
    else:
        return 0

def weight6(x):
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 6
    else:
        return 0

def diabetes(x):
    if math.isnan(x):
        return math.nan
    if x == 1 or x == 2:
        return 1
    else:
        return 0