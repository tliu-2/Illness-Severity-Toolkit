# This file contains all the necessary values / whatever that are required to calculate APACHE scores.
import math


# Contains all the functions / methods/ defs that calculate the APACHE scores for each category.
# These functions are meant to be used in a .apply setting

def get_heart_rate_score(heart_rate, heart_rate_1=None):
    """
    Assigns an APACHE score for heart rate
    :param heart_rate: 24h heart rate variable
    :param heart_rate_1: alternative heart rate variable used if heart_rate is missing
    :return: APACHE score for given heart rate
    """
    if math.isnan(heart_rate):
        if heart_rate_1 is not None:
            if math.isnan(heart_rate_1):
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
    """
    if math.isnan(bp):
        if bp_1 is not None:
            if math.isnan(bp_1):
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
    """
    if math.isnan(temp):
        if temp_1 is not None:
            if math.isnan(temp_1):
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
    """
    if math.isnan(rr):
        if rr_1 is not None:
            if math.isnan(rr_1):
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
    elif (6 <= rr <= 11) & (mech_vent == 0):
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


def get_aado2(po2, fio2, pco2, isMechVent):
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
    # Check if patient is mechanically ventilated and has an fiO2 level >= 0.5
    elif (isMechVent == 1) & (fio2 / 100 >= 0.5):
        # Calculate A - aDO2:
        a = (((fio2 / 100) * 713) - (pco2 / 0.8))
        gradient_dif = (a - po2)
        return getAaDO2APACHE(gradient_dif)
    else:  # Patient not mechanically ventilated / not have a fiO2 level of at least 0.5
        return 0


# This method is solely used when a patient is mechanically ventilated and has a fiO2 <= 0.5
# @param score is a panda Series containing the calculated AaDO2 value.
# @return APACHE values for a calculated value.
def getAaDO2APACHE(score):
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
def get_hematocrit(hct, hct_d0=None, hct_d1=None):
    """
    Assigns an APACHE score based on hematocrit measurements. Assumes if hct_d0 is missing then hct_d1 is also missing.
    :param hct: 24h hematocrit values
    :param hct_d0: d0 alternative value if 24h is missing
    :param hct_d1: d1 alternative value if both d0 and 24h are missing
    :return: APACHE score based on hematocrit measurements
    """
    if math.isnan(hct):
        if hct_d0 is not None:
            if math.isnan(hct_d0):
                if hct_d1 is not None:
                    if math.isnan(hct_d1):
                        return math.nan
                    else:
                        hct = hct_d1
                else:
                    return math.nan
            else:
                hct = hct_d0
        else:
            return math.nan

    if 41 <= hct <= 49:
        return 0
    else:
        return 3


# WBC count:
# This method converts white blood cell counts (WBC) into APACHE scores.
# @param wbcCount is a panda Series containing patient values of white blood cell count.
# @return score is a panda Series containing APACHE score values for white blood cell counts.
def get_wbc(wbc, wbc_d0=None, wbc_d1=None):
    """
    Assigns an APACHE score based on wbc measurements.
    :param wbc: 24h wbc value
    :param wbc_d0: d0 alternative if 24h is missing
    :param wbc_d1: d1 alternative if both 24h and d0 are missing
    :return:
    """
    if math.isnan(wbc):
        if wbc_d0 is not None:
            if math.isnan(wbc_d0):
                if wbc_d1 is not None:
                    if math.isnan(wbc_d1):
                        return math.nan
                    else:
                        wbc = wbc_d1
                else:
                    return math.nan
            else:
                wbc = wbc_d0
        else:
            return math.nan

    if wbc >= 25 or 1.0 <= wbc <= 2.9:
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


def get_cr(cr, aki):
    """
    Assigns an APACHE score for creatinine values and kidney failure.
    :param cr: Creatinine values
    :param aki: Acute kidney injury status
    :return: apache score
    """
    if math.isnan(cr):
        return math.nan
    if not aki:
        if cr >= 1.95:
            return 7
        elif 1.5 <= cr <= 1.94:
            return 4
        elif cr <= 0.4:
            return 3
        else:
            return 0
    else:
        if cr >= 1.5:
            return 10
        else:
            return 0

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

def get_bun(bun, bun_d1=None):
    """
    Assigns an APACHE score for given Blood Urea Nitrogen (BUN) values
    :param bun: 24h bun values
    :param bun_d1: alternative bun values if 24h values are missing
    :return: APACHE score for given values
    """
    if math.isnan(bun):
        if bun_d1 is not None:
            if math.isnan(bun_d1):
                return math.nan
            else:
                bun = bun_d1
        else:
            return math.nan

    if bun <= 16.9:
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
def get_na(na, na1=None):
    """
    Assigns an APACHE score for given serum sodium values.
    :param na: 24h sodium values
    :param na1: alternative sodium values if 24h is missing
    :return: APACHE scores for given values
    """
    if math.isnan(na):
        if na1 is not None:
            if math.isnan(na1):
                return math.nan
            else:
                na = na1
        else:
            return math.nan

    if na >= 155:
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
    if math.isnan(alb):
        if alb_d1 is not None:
            if math.isnan(alb_d1):
                return math.nan
            else:
                alb = alb_d1
        else:
            return math.nan

    if alb >= 4.5:
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
    if math.isnan(bili):
        if bili_d1 is not None:
            if math.isnan(bili_d1):
                return math.nan
            else:
                bili = bili_d1
        else:
            return math.nan

    if bili >= 8.0:
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
    if math.isnan(glucose):
        if gluc_d1 is not None:
            if math.isnan(gluc_d1):
                return math.nan
            else:
                glucose = gluc_d1
        else:
            return math.nan

    if glucose >= 330:
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

def check_cirr(cirr):
    """
    Assigns an APACHE score for cirrhosis
    :param cirr: cirrhosis status
    :return: APACHE score based on whether a subject has cirrhosis or not.
    """
    if math.isnan(cirr):
        return math.nan
    elif cirr == 1:
        return 4
    else:
        return 0


# This method checks if the patient has cancer.

def check_cancer(cancer):
    """
    Assigns an APACHE score for a given cancer status.
    :param cancer: cancer status
    :return: APACHE score based on whether a subject has cancer.
    """
    # Unable to check for type of cancer, APACHE score will be off +- 3
    # This program will assume the worst meaning if cancer == yes, use score of Lymphoma
    if math.isnan(cancer):
        return math.nan
    elif cancer == 1:
        return 11
    else:
        return 0

def check_leukemia(status):
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 10
    else:
        return 0

def check_lymphoma(status):
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 13
    else:
        return 0

def check_immuno_sup(immunosup):
    """
    Assigns apache score based on immunocompromised status
    :param immunosup: immunocompromised status
    :return: apache score
    """
    if math.isnan(immunosup):
        return math.nan
    elif immunosup == 1:
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
    if math.isnan(status):
        return math.nan
    elif status == 1:
        return 23
    else:
        return 0
