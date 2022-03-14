import pandas as pd
import numpy as np
import math


def get_resp(pao2, fio2, intubated):
    if math.isnan(pao2) or math.isnan(fio2):
        return math.nan
    ratio = (pao2 / fio2) * 100
    if ratio > 400:
        return 0
    elif 301 <= ratio <= 400:
        return 1
    elif ratio <= 300:
        if (100 < ratio <= 200) and intubated == 1:
            return 3
        elif ratio <= 100 and intubated == 1:
            return 4
        elif ratio > 200:
            return 2


def get_platlets(plts):
    if math.isnan(plts):
        return math.nan
    if plts > 150:
        return 0
    elif 101 <= plts <= 150:
        return 1
    elif 51 <= plts <= 100:
        return 2
    elif 21 <= plts <= 50:
        return 3
    elif plts <= 20:
        return 4

def get_bilirubin(bili):
    if math.isnan(bili):
        return math.nan
    elif bili < 1.2:
        return 0
    elif 1.2 <= bili <= 1.9:
        return 1
    elif 2 <= bili <= 5.9:
        return 2
    elif 6 <= bili <= 11.9:
        return 3
    elif bili > 12:
        return 4

def get_bp(bp, dbamine, dpamine, norepi, epi):
    if math.isnan(bp):
        return math.nan

    if math.isnan(dbamine) and math.isnan(dpamine) and math.isnan(norepi) and math.isnan(epi):
        if bp >= 70:
            return 0
        elif bp < 70:
            return 1

    
