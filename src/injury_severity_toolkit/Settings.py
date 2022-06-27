# This file contains all the necessary values / whatever that are required to calculate APACHE scores.
import math
from datetime import datetime, date
from tkinter import filedialog

import pandas as pd


def export_csv(df):
    exportfile = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv(exportfile, index=None, header=True)


def sofa_export_csv(df):
    exportfile = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv(exportfile, index=True, header=True)

# Contains all the functions / methods/ defs that calculate the APACHE scores for each category.
# These functions are meant to be used in a .apply setting

def get_heart_rate_score(heart_rate, heart_rate_1=None):
    """
    Assigns an APACHE score for heart rate
    :param heart_rate: 24h heart rate variable
    :param heart_rate_1: alternative heart rate variable used if heart_rate is missing
    :return: APACHE score for given heart rate

    >>> get_heart_rate_score(170)
    17
    >>> get_heart_rate_score(math.nan, 102)
    1
    >>> get_heart_rate_score(42)
    5
    >>> get_heart_rate_score(114)
    5
    >>> get_heart_rate_score(math.nan, 116)
    5
    >>> get_heart_rate_score(65)
    0
    """
    if math.isnan(heart_rate) or heart_rate == -99:
        if heart_rate_1 is not None:
            if math.isnan(heart_rate_1) or heart_rate_1 == -99:
                return math.nan
            else:
                heart_rate = heart_rate_1
        else:
            return math.nan

    if heart_rate >= 155:
        return 17
    elif 154 >= heart_rate >= 140:
        return 13
    elif 139 >= heart_rate >= 120:
        return 7
    elif 119 >= heart_rate >= 110 or 49 >= heart_rate >= 40:
        return 5
    elif 109 >= heart_rate >= 100:
        return 1
    elif heart_rate <= 39:
        return 8
    else:
        return 0


# Mean Blood Pressure:

def get_bp_score(bp, bp_1=None):
    """
    Assigns an APACHE score for blood pressure
    :param bp: 24h mean arterial blood pressure value
    :param bp_1: alternative variable if 24h variable is missing
    :return: APACHE score for given blood pressure

    >>> get_bp_score(170)
    10
    >>> get_bp_score(90)
    0
    >>> get_bp_score(math.nan, 62)
    7
    >>> get_bp_score(125)
    7
    """
    if math.isnan(bp) or bp == -99:
        if bp_1 is not None:
            if math.isnan(bp_1) or bp_1 == -99:
                return math.nan
            else:
                bp = bp_1
        else:
            return math.nan

    if bp >= 140:
        return 10
    elif 130 <= bp <= 139:
        return 9
    elif 120 <= bp <= 129 or 60 <= bp <= 69:
        return 7
    elif 100 <= bp <= 119:
        return 4
    elif 70 <= bp <= 79:
        return 6
    elif 40 <= bp <= 59:
        return 15
    elif bp <= 39:
        return 23
    else:
        return 0


# Temperature:
def get_temp_score(temp, temp_1=None):
    """
    Assigns an APACHE score for temperatures
    :param temp: 24h temperature value
    :param temp_1: alternative if 24h variable is missing / null
    :return: APACHE score for given temperature

    >>> get_temp_score(37)
    0
    >>> get_temp_score(math.nan, 33.2)
    16
    >>> get_temp_score(42)
    4
    """
    if math.isnan(temp) or temp == -99:
        if temp_1 is not None:
            if math.isnan(temp_1) or temp_1 == -99:
                return math.nan
            else:
                temp = temp_1
        else:
            return math.nan

    if temp >= 40:
        return 4
    elif 35 <= temp <= 35.9:
        return 2
    elif 34 <= temp <= 34.9:
        return 8
    elif 33.5 <= temp <= 33.9:
        return 13
    elif 33 <= temp <= 33.4:
        return 16
    elif temp <= 32.9:
        return 20
    else:
        return 0


# Respiratory Rate:
# To do:
# Add conditionals for mechanically ventilated patients. DONE

# Grabs APACHE scores for respiratory rates for each patient.
# @param respRate is a panda Series containing respiratory rate values.
# @ return respiratoryRate is a panda Series that contains respRate values in APACHE score values.

def get_rr_score(rr, mech_vent, rr_1=None):
    """
    Assigns an APACHE score for respiratory rate
    :param rr: 24h respiratory rate value
    :param mech_vent: mechanical ventilation status at 8am
    :param rr_1: alternative if 24h variable is missing / null
    :return: APACHE score for given respiratory rate

    >>> get_rr_score(15, 1)
    0
    >>> get_rr_score(15, 0)
    0
    >>> get_rr_score(7, 4)
    8
    >>> get_rr_score(7, 5)
    0
    """
    if math.isnan(rr) or rr == -99:
        if rr_1 is not None:
            if math.isnan(rr_1) or rr_1 == -99:
                return math.nan
            else:
                rr = rr_1
        else:
            return math.nan

    if rr >= 50:
        return 18
    elif 40 <= rr <= 49:
        return 11
    elif 35 <= rr <= 39:
        return 9
    elif 25 <= rr <= 34:
        return 6
    elif 12 <= rr <= 13:
        return 7
    elif (6 <= rr <= 11) & (mech_vent == 0):  # If not invasive mechanically ventilated give score.
        return 8
    elif rr <= 5:
        return 17
    else:
        return 0


def get_mech_vent(mech_vent):
    """
    Returns 1 if subject is on IMV and 0 if not
    :param mech_vent: mechanical ventilation status
    :return: 1 if mechanically ventilated, 0 if not
    """
    if math.isnan(mech_vent):
        return math.nan
    elif mech_vent == 0:
        return 0
    else:
        return 1


def get_aa_or_pao2(aa, pao2):
    """
    Calculates apache score based on aado2 or pao2 depending on availability.
    :param aa: aado2 values
    :param pao2: pao2 values
    :return: apache score
    """
    if math.isnan(aa) and math.isnan(pao2):
        return math.nan
    if math.isnan(aa):
        if pao2 >= 80:
            return 0
        elif 70 <= pao2 <= 79:
            return 2
        elif 50 <= pao2 <= 69:
            return 5
        else:
            return 15
    else:
        if aa < 100:
            return 0
        elif 100 <= aa <= 249:
            return 7
        elif 250 <= aa <= 349:
            return 9
        elif 350 <= aa <= 499:
            return 11
        else:  # aa >= 500:
            return 14


def get_aado2(po2, fio2, pco2, mech_vent):
    """
    Assigns an aado2 for patients who are mechanically ventilated and have an fio2 >= 50%. If the patient isn't
    mechanically ventilated return 0 and use po2 APACHE score instead.
    :param po2: 24h / d0 value for po2
    :param fio2: abg fio2 value
    :param pco2: 24h / d0 ph value for po2
    :param isMechVent: mechanical ventiliation status
    :return: APACHE score based on aado2 value
    """
    if math.isnan(po2) or math.isnan(fio2) or math.isnan(pco2):
        return math.nan
    if po2 == -99 or fio2 == -99 or pco2 == -99:
        return math.nan
    # Check if patient is mechanically ventilated and has an fiO2 level >= 0.5
    if (mech_vent == 1) and (fio2 >= 0.5):
        # Calculate A - aDO2:
        a = ((fio2 * 713) - (pco2 / 0.8))
        gradient_dif = (a - po2)
        return get_aa_score(gradient_dif)
    else:  # Patient not mechanically ventilated / not have a fiO2 level of at least 0.5
        return get_pao2(po2, mech_vent)


# This method is solely used when a patient is mechanically ventilated and has a fiO2 <= 0.5
# @param score is a panda Series containing the calculated AaDO2 value.
# @return APACHE values for a calculated value.
def get_aa_score(score):
    """
    Helper to the aado2 function - actually Assigns the APACHE score based on an aado2 value.
    :param score: calculated aado2 value
    :return: APACHE score based on the passed value
    """
    if score < 100:
        return 0
    elif 100 <= score <= 249:
        return 7
    elif 250 <= score <= 349:
        return 9
    elif 350 <= score <= 499:
        return 11
    else:  # score >= 500:
        return 14


def get_pao2(po2, mech_vent, po2_1=None):
    """
    Assigns an APACHE score for po2. Only used when patient is not mechanically ventilated.
    :param po2: 24h / d0 po2 value
    :param mech_vent: mechanical ventilation status
    :param po2_1: alternative po2 value if 24h / d0 is missing
    :return: APACHE score based on either po2 or po2_1
    """
    if mech_vent == 0:
        if po2_1 is not None:
            if math.isnan(po2):
                if math.isnan(po2_1):
                    return math.nan
                else:
                    po2 = po2_1
        else:
            return math.nan

        if po2 >= 80:
            return 0
        elif 70 <= po2 <= 79:
            return 2
        elif 50 <= po2 <= 69:
            return 5
        else:
            return 15
    else:
        return 0


# Hematocrit:
# This method converts hematocrit measurements into APACHE scores.
# @param critScore is a panda Series that contains patient values for Hematocrit
# @return score is a panda Series that contains APACHE values for a corresponding hematocrit level in patients.
def get_hematocrit(hct):
    """
    Assigns an APACHE score based on hematocrit measurements. Assumes if hct_d0 is missing then hct_d1 is also missing.
    :param hct: 24h hematocrit values
    :return: APACHE score based on hematocrit measurements
    """
    if math.isnan(hct) or hct == -99:
        return math.nan
    elif 41 <= hct <= 49:
        return 0
    else:
        return 3


# WBC count:
# This method converts white blood cell counts (WBC) into APACHE scores.
# @param wbcCount is a panda Series containing patient values of white blood cell count.
# @return score is a panda Series containing APACHE score values for white blood cell counts.
def get_wbc(wbc):
    """
    Assigns an APACHE score based on wbc measurements.
    :param wbc: 24h wbc value
    :param wbc_d0: d0 alternative if 24h is missing
    :param wbc_d1: d1 alternative if both 24h and d0 are missing
    :return:
    """
    if math.isnan(wbc) or wbc == -99:
        return math.nan
    elif wbc >= 25 or 1.0 <= wbc <= 2.9:
        return 5
    elif 20 <= wbc <= 24.9:
        return 1
    elif wbc < 1.0:
        return 19
    else:
        return 0


# .....
# If AKI use s/
# If no AKI use c/
def check_kidney_failure(cr_high, urine_out, esrd):
    """
    Checks if a subject has kidney failure based on their creatinine, urine output, and end stage renal disease status.
    :param cr_high: high creatinine values in 24h
    :param urine_out: urine output in 24h
    :param esrd: end stage renal disease status
    :return: true or false based on these values.
    """
    if cr_high > 1.5 and urine_out < 410 and esrd == 1:  # Consider removing urine_out
        return True
    else:
        return False


# This method specifically calculates the score of patients for the Creatinine category
# @param crLevel is the corresponding crLevel of the patient from the .csv file.
# @param AKIStatus is a Panda Series containing booleans of a patients status of AKI / ARF.
# @return A Panda Series containing scores for patients Creatinine levels.


def get_cr(cr, arf):
    """
    Assigns an APACHE score for creatinine values and kidney failure.
    :param cr: Creatinine values
    :param aki: Acute kidney injury status
    :return: apache score
    """
    if math.isnan(cr) or cr == -99:
        return math.nan

    if arf:
        if cr >= 1.5:
            return 10
        else:
            return 0
    else:  # ARF == false
        if cr >= 1.95:
            return 7
        elif 1.5 <= cr <= 1.94:
            return 4
        elif cr <= 0.4:
            return 3
        else:
            return 0

    # if not arf:  # If subject does not have ARF
    #     if cr >= 1.95:
    #         return 7
    #     elif 1.5 <= cr <= 1.94:
    #         return 4
    #     elif cr <= 0.4:
    #         return 3
    #     else:
    #         return 0
    # else:  # Subject has arf
    #     if cr >= 1.5:
    #         return 10
    #     else:
    #         return 0


def get_urine(urine):
    if math.isnan(urine) or urine == -99:
        return math.nan
    if urine >= 4000:
        return 1
    elif 2000 <= urine <= 3999:
        return 0
    elif 1500 <= urine <= 1999:
        return 4
    elif 900 <= urine <= 1499:
        return 5
    elif 600 <= urine <= 899:
        return 7
    elif 400 <= urine <= 599:
        return 8
    elif urine <= 399:
        return 15


def get_cr2(cr, aki, cr_1=None):
    """
    Assigns an APACHE score for creatinine values and kidney failure.
    :param cr: 24h creatinine values
    :param aki: kidney failure status
    :param cr_1: alternative creatinine values if 24h is missing
    :return: APACHE score based on creatinine and kindey failure.
    """
    if math.isnan(cr):
        if cr_1 is not None:
            if math.isnan(cr_1):
                return math.nan
            else:
                cr = cr_1
        else:
            return math.nan

    if not aki:  # use s/ Creatinine
        if cr >= 1.95:
            return 7
        elif 1.5 <= cr <= 1.94:
            return 4
        elif cr <= 0.4:
            return 3
        else:
            return 0
    else:  # AKIStatus == false
        if cr >= 1.5:
            return 10
        else:
            return 0


# ....

# BUN: (Blood Urea Nitrogen) mg/dL
# This method converts BUN levels into APACHE scores.

def get_bun(bun):
    """
    Assigns an APACHE score for given Blood Urea Nitrogen (BUN) values
    :param bun: 24h bun values
    :param bun_d1: alternative bun values if 24h values are missing
    :return: APACHE score for given values
    """
    if math.isnan(bun) or bun == -99:
        return math.nan
    elif bun <= 16.9:
        return 0
    elif 17 <= bun <= 19:
        return 2
    elif 20 <= bun <= 39:
        return 7
    elif 40 <= bun <= 79:
        return 11
    else:  # bun[x] >= 80
        return 12


# Sodium:
# This method converts serum sodium levels into APACHE scores.
# @param naLevel is a panda Series that patient values for sodium concentration in serum.
# @return score is a panda Series that contains APACHE score values for corresponding sodium concentrations.
def get_na(na):
    """
    Assigns an APACHE score for given serum sodium values.
    :param na: 24h sodium values
    :param na1: alternative sodium values if 24h is missing
    :return: APACHE scores for given values
    """
    if math.isnan(na) or na == -99:
        return math.nan
    elif na >= 155:
        return 4
    elif 120 <= na <= 134:
        return 2
    elif na <= 119:
        return 3
    else:
        return 0


# Albumin: g/dL?
# This method converts serum albumin levels into APACHE scores.
# @param albLevel is a panda Series that contains patient values for albumin levels in serum.
# @return score is a panda Series that contains APACHE score values for corresponding albumin levels.
def get_alb(alb, alb_d1=None):
    """
    Assigns an APACHE score for given serum albumin values.
    :param alb: 24h albumin values
    :param alb_d1: alternative albumin values if 24h values are missing
    :return: APACHE score based on the given values.
    """
    if math.isnan(alb) or alb == -99:
        return math.nan
    elif alb >= 4.5:
        return 4
    elif 2.0 <= alb <= 2.4:
        return 6
    elif alb <= 1.9:
        return 11
    else:
        return 0


# Bilirubin: mg/dL
# This method assigns bilirubin measurements to an APACHE score.
# @param bilirubinLevels is a panda Series containing patient values for bilirubin in serum.
# @return score is a panda Series containing APACHE score values for corresponding bilirubin levels.

def get_bilirubin(bili, bili_d1=None):
    """
    Assigns an APACHE score for given bilirubin values
    :param bili: 24h / d0 bilirubin values
    :param bili_d1: alternative bilirubin values if 24h / d0 are missing
    :return: APACHE score based on values
    """
    if math.isnan(bili) or bili == -99:
        return math.nan
    elif bili >= 8.0:
        return 16
    elif 3.0 <= bili <= 4.9:
        return 6
    elif 2.0 <= bili <= 2.9:
        return 5
    else:
        return 0


# Glucose: mg/dL
# This method assigns an APACHE score to a measurement of serum glucose.
# @param glucose is a panda Series containing pateint values of glucose in serum.
# @return scores is a panda Series containing APACHE score values for corresponding glucose levels.

def get_glucose(glucose, gluc_d1=None):
    """
    Assigns an APACHE score for given glucose values
    :param glucose: 24h / d0 glucose values
    :param gluc_d1: alternative glucose values if 24h / d0 are missing
    :return: APACHE score based on given values.
    """
    if math.isnan(glucose) or glucose == -99:
        return math.nan
    elif glucose >= 330:
        return 5
    elif 200 <= glucose <= 349:
        return 3
    elif 40 <= glucose <= 59:  # Special Conditions apply, ask Carmen / Eric
        return 9
    elif glucose <= 39:
        return 8
    else:
        return 0


# The following scores are for Figures 2 and 3.


# pH and pCO2:
# This method converts a pH and pCO2 into APACHE-unit scores.
# @param pH is a Panda Series containing the blood pH of patients.
# @param pCO2 is a Panda Series containing the pCO2 levels of patients.
# @return a Panda Series containing APACHE-unit scores for these two categories.
def get_ph_pco2(ph, pco2):
    """
    Assigns an APACHE score for given pH and pCO2 values.
    :param ph: 24h / d0 pH values
    :param pco2: 24h / d0 pCO2 values
    :return: APACHE score based on given values.
    """
    if math.isnan(ph) or math.isnan(pco2):
        return math.nan
    if ph == -99 or pco2 == -99:
        return math.nan
    elif ph < 7.2:
        if pco2 < 50:
            return 12
        else:
            return 4
    elif 7.20 <= ph < 7.30:
        if pco2 < 30:
            return 9
        elif 30 <= pco2 < 40:
            return 6
        elif 40 <= pco2 < 50:
            return 3
        else:
            return 2
    elif 7.30 <= ph < 7.50:
        if pco2 < 30:
            if ph < 7.35:
                return 9
            else:
                return 5
        elif 30 <= pco2 < 45:
            if ph >= 7.45:
                if 35 <= pco2 < 45:
                    return 2
                else:
                    return 0
            else:
                return 0
        elif pco2 >= 45:
            if ph >= 7.45:
                return 12
            else:
                return 1
    elif 7.50 <= ph:
        if pco2 < 40:
            if ph >= 7.60:
                return 0
            else:
                return 3
        else:
            return 12


# Cormobidities: Cirhosis, Leukemnia, Age, etc.
# This method convers a patients age into a corresponding score.
# @param age is a Panda Series containing the age of all patients.
# @return a Panda Series containing the age in APACHE-unit scores.

def calculate_age_from_dob(dob):
    """
    Calculates an age in years from a dob in the format of YYYY-mm-dd. Will add try-except for multiple format support.
    :param dob: date of birth in YYYY-mm-dd format
    :return: age in years
    """
    if pd.isnull(dob):
        return math.nan
    now = date.today()
    dob = datetime.strptime(dob, "%Y-%m-%d")
    age = now.year - dob.year - ((now.month, now.day) < (dob.month, dob.day))
    return age


def get_age(age):
    """
    Assigns an APACHE score for a given age.
    :param age: age of the subject
    :return: APACHE score based on age.
    """
    if math.isnan(age):
        return math.nan
    elif age >= 85:
        return 24
    elif 75 <= age <= 84:
        return 17
    elif 70 <= age <= 74:
        return 16
    elif 65 <= age <= 69:
        return 13
    elif 60 <= age <= 64:
        return 11
    elif 45 <= age <= 59:
        return 5
    else:
        return 0


# This method checks if the patient has cirrhosis.

def check_cirr(status):
    """
    Assigns an APACHE score for cirrhosis
    :param status: cirrhosis status
    :return: APACHE score based on whether a subject has cirrhosis or not.
    """
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 4
    else:
        return 0


# This method checks if the patient has cancer.

def check_cancer(status):
    """
    Assigns an APACHE score for a given cancer status.
    :param status: cancer status
    :return: APACHE score based on whether a subject has cancer.
    """
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 11
    else:
        return 0


def check_leukemia(status):
    """
    Assigns an APACHE score for a given leukemia status.
    :param status: leukemia status
    :return: APACHE score based on whether a subject has leukemia.
    """
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 10
    else:
        return 0


def check_lymphoma(status):
    """
    Assigns an APACHE score for a given lymphoma status.
    :param status: lymphoma status
    :return: APACHE score based on whether a subject has lymphoma.
    """
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 13
    else:
        return 0


def check_immuno_sup(status):
    """
    Assigns apache score based on immunocompromised status
    :param status: immunocompromised status
    :return: apache score
    """
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 10
    else:
        return 0


# This method checks if the patient is immuno-suppressed.

def check_immuno_sup2(organtx, sct, prednisone):
    """
    Assigns an APACHE score based on immunocompromised / suppressed status
    :param organtx: orgran transplant status
    :param sct: stem cell transplant status
    :param prednisone: prednisone status
    :return: APACHE score
    """
    if math.isnan(organtx) and math.isnan(sct) and math.isnan(prednisone):
        return math.nan
    elif organtx == 1 or sct == 1 or prednisone == 1:
        return 10
    else:
        return 0


# Glasgow Coma Scale:
# As per the article: eliminating the distinctions between incomprehensible words and inappropriate sounds,
# Hexion withdrawal and decorticate rigidity, and decerebrate rigidity and no responses,
# and by simplifying the evaluation of eye opening

# This method converts the visual score into the simplified scores.

def gcs_visual(visual):
    """
    Simplifies gcs visual scores based on the 1991 APACHE III Paper
    :param visual: gcs visual score
    :return: simplified gcs visual score
    """
    if math.isnan(visual):
        return math.nan
    elif visual > 1:  # Spontaneous eye opening.
        return 2
    else:
        return 1  # No response


# Due to the article's simplification of certain scores, the scoring will look like this:
# Decerebrate rigidity and no response are combined to a score of "1" and the pain responses are combined to "3".
# This method converts motor scores into the simplified scores.

def gcs_motor(motor):
    """
    Simplifies gcs motor scores based on the 1991 APACHE III Paper
    :param motor: gcs motor score
    :return: simplified gcs motor score
    """
    if math.isnan(motor):
        return math.nan
    elif motor == 1 or motor == 2:  # No response and Decerebrate Rigidity
        return 1
    elif motor == 3 or motor == 4:
        return 2
    elif motor == 5:  # Any pain response
        return 3
    else:
        return 4


# This method converts verbal scores into the simplified scores given in the article.

def gcs_verbal(verbal):
    """
    Simplifies gcs verbal scores based on the 1991 APACHE III Paper
    :param verbal: gcs verbal score
    :return: simplified gcs verbal score
    """
    if math.isnan(verbal):
        return math.nan
    elif verbal == 1:
        return 1
    elif verbal == 2 or verbal == 3:  # Incomprehensible / inappropriate
        return 2
    elif verbal == 4:
        return 3
    else:
        return 4


# This method is converts the Glasgow Coma scores into APACHE scores.

def gcs_combined(visual, motor, verbal):
    """
    Assigns an APACHE score based on the combination of the simplified gcs scores
    :param visual: simplified gcs visual score
    :param motor: simplified gcs motor score
    :param verbal: simplified gcs verbal score
    :return: APACHE score
    """
    if visual == 2:  # spontaneous eye opening
        if verbal == 4:  # verbal is oriented
            if motor == 4:  # obeys verbal command
                return 0
            else:
                return 3
        elif verbal == 3:  # verbal is confused
            if motor == 4:
                return 3
            elif motor == 3:  # Any pain response
                return 8
            else:
                return 13
        elif verbal == 2:  # Incomprehensible / inappropriate
            if motor == 4:
                return 10
            elif motor == 3:  # Any pain response
                return 13
            elif motor == 2:
                return 24
            else:  # No response / decerebrate rigidity
                return 29
        elif verbal == 1:  # No response (verbal)
            if motor == 4 or motor == 3:
                return 15
            elif motor == 2:
                return 24
            else:
                return 29
    else:  # Eyes do not open spontaneuosly
        if verbal == 2:
            if motor == 2:
                return 24
            elif motor == 1:
                return 29
        elif verbal == 1:
            if motor == 4 or motor == 3:
                return 16
            elif motor == 2:
                return 33
            elif motor == 1:
                return 48
            else:
                return math.nan


def check_aids(status):
    """
    Calculate APACHE score given a binary status code for AIDS
    :param status: AIDS status of patient
    :return: APACHE score
    """
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 23
    else:
        return 0


# -----------------------------------------------------------------------------------------------------------------------
# CCI Start:
def cci_get_age_score(age):
    """
    Gets the CCI for age.
    :param age: Age
    :return: CCI for age.
    """
    if math.isnan(age):
        return math.nan
    if age >= 80:
        return 4
    elif 70 <= age <= 79:
        return 3
    elif 60 <= age <= 69:
        return 2
    elif 50 <= age <= 59:
        return 1
    else:  # age < 50
        return 0


def cci_weight1(x):
    """
    Gets the CCI for categories designated as "1 weight".
    :param x: Category (e.g., heart rate or something)
    :return: CCI for x category.
    """
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 1
    else:  # x == 0
        return 0


def cci_weight2(x):
    """
    Gets the CCI for categories designated as "2 weight".
    :param x: Category
    :return: CCI for x category.
    """
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 2
    else:
        return 0


def cci_weight3(x):
    """
    Gets the CCI for categories designated as "3 weight".
    :param x: Category
    :return: CCI for x category.
    """
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 3
    else:
        return 0


def cci_weight6(x):
    """
    Gets the CCI for categories designated as "6 weight".
    :param x: Category
    :return: CCI for x category.
    """
    if math.isnan(x):
        return math.nan
    if x == 1:
        return 6
    else:
        return 0


# ----------------------------------------------------------------------------------------------------------------------
# SOFA Start:
def sofa_resp(pao2, fio2, mv):
    """
    Calculate SOFA scores for the respiratory section.
    :param pao2: Partial pressure of oxygen (mmHg)
    :param fio2: Fraction of inspired oxygen (decimal)
    :param mv: mechanical ventilation status
    :return: SOFA score
    """
    if math.isnan(pao2) or math.isnan(fio2):
        return math.nan
    if pao2 == -99 or fio2 == -99:
        return math.nan

    ratio = (pao2 / fio2)
    if ratio > 400:
        return 0
    elif 301 <= ratio <= 400:
        return 1
    elif ratio <= 300:
        if (101 <= ratio <= 200) and mv == 1:
            return 3
        elif ratio <= 100 and mv == 1:
            return 4
        elif mv == 0 or ratio > 200:
            return 2


def sofa_platelets(plts):
    """
    Calculates SOFA score for platelets section.
    :param plts: platelets measurement
    :return: SOFA score
    """
    if math.isnan(plts) or plts == -99:
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


def sofa_bilirubin(bili):
    """
    Calculates SOFA score for bilirubin section.
    :param bili: bilirubin measurement
    :return: SOFA score
    """
    if math.isnan(bili) or bili == -99 or bili == -99.9:
        return math.nan
    if bili < 1.2:
        return 0
    elif 1.2 <= bili <= 1.9:
        return 1
    elif 2 <= bili <= 5.9:
        return 2
    elif 6 <= bili <= 11.9:
        return 3
    elif bili >= 12:
        return 4


def sofa_bp(bp, pressors):
    """
    Calculates SOFA scores for blood pressure section.
    :param bp: blood pressure measurement
    :param pressors: measurement for pressors
    :return: SOFA score
    """
    if math.isnan(bp):
        return math.nan

    if bp >= 70 and math.isnan(pressors):
        return 0
    else:  # bp < 70
        if math.isnan(pressors):
            return 1
        elif pressors == 1:
            return 2
        elif pressors == 2:
            return 3
        elif pressors == 3:
            return 4


def sofa_gcs(gcs):
    """
    Calculates SOFA score for Glasgow Coma Scale (gcs) section.
    :param gcs: Glasgow Coma Scale
    :return: SOFA score
    """
    if math.isnan(gcs) or gcs == -99:
        return math.nan
    if gcs >= 15:
        return 0
    elif 13 <= gcs <= 14:
        return 1
    elif 10 <= gcs <= 12:
        return 2
    elif 6 <= gcs <= 9:
        return 3
    else:  # gcs < 6
        return 4


def sofa_renal(cr, urine):
    """
    Calculates SOFA score for the renal section.
    :param cr: Creatinine measurement
    :param urine: Urine output measurement
    :return: SOFA score
    """
    if math.isnan(cr) and math.isnan(urine):
        return math.nan
    if cr < 1.2:
        return 0
    elif 1.2 <= cr <= 1.9:
        return 1
    elif 2 <= cr <= 3.4:
        return 2
    else:
        if math.isnan(cr):
            if 200 <= urine <= 500:
                return 3
            elif urine < 200:
                return 4
        else:  # creatinine is not nan
            if 3.5 <= cr <= 4.9:
                return 3
            else:  # cr > 5
                return 4
