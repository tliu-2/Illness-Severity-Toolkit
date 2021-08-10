# This program calculates the APACHE score of a patients on using their Day 0 statistics.
# How it works:
# This program functions by taking an entire column of patient data in a .csv file and assigns all the measurements
# in the column to its respective APACHE score for that individual measurement. (using panda Series)
# This data is then placed into a Pandas' database. The program then utilizes the dataframe.sum(axis) method
# (axis = 1) such that the row values are summed (total score for an individual).

import pandas as pd
# mport Settings_CHROME_Batch as Settings
import Settings_CHROME_Batch as Settings


def run(dataset):
    sumdf = pd.DataFrame([])
    #  PROTOTYPE .APPLY VARIANT FOR APACHE CALC
    temp_high = pd.Series([])
    temp_low = pd.Series([])

    sumdf['Age'] = dataset.age.apply(Settings.get_age)
    sumdf['Cirrhosis'] = dataset.cirrhosisStatus.apply(Settings.check_cirr)
    sumdf['Cancer'] = dataset.cancerStat.apply(Settings.check_cancer)

    sumdf['organtx'] = dataset.organtx
    sumdf['sct'] = dataset.sct
    sumdf['hiv'] = dataset.hiv
    sumdf['cd4'] = dataset.cd4
    sumdf['prednisone'] = dataset.prednisone
    sumdf['Immunosuppression'] = sumdf.apply(lambda x: Settings.check_immuno_sup(x['organtx'], x['sct'], x['prednisone']), axis=1)
    sumdf['HIV / AIDS'] = sumdf.apply(lambda x: Settings.check_hiv_aids(x['hiv'], x['cd4']), axis=1)
    sumdf = sumdf.drop(columns=['organtx', 'sct', 'hiv', 'cd4', 'prednisone'])

    temp_high['Heart Rate High'] = dataset.pulseHigh.apply(Settings.get_heart_rate_score)
    temp_low['Heart Rate Low'] = dataset.pulseLow.apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate'] = temp_high['Heart Rate High'].combine(temp_low['Heart Rate Low'], max, fill_value=0)

    temp_high['High BP'] = dataset.bpHigh.apply(Settings.get_bp_score)
    temp_low['Low BP'] = dataset.bpLow.apply(Settings.get_bp_score)
    sumdf['Blood Pressure'] = temp_high['High BP'].combine(temp_low['Low BP'], max, fill_value=0)

    temp_high['High Temp'] = dataset.temperatureHigh.apply(Settings.get_temp_score)
    temp_low['Low Temp'] = dataset.temperatureLow.apply(Settings.get_temp_score)
    sumdf['Temperature'] = temp_high['High Temp'].combine(temp_low['Low Temp'], max, fill_value=0)

    sumdf['High RR'] = dataset.respRateHigh
    sumdf['Low RR'] = dataset.respRateLow
    sumdf['Mech Vent'] = dataset.isMechVent

    sumdf['High RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['High RR'], x['Mech Vent']), axis=1)
    sumdf['Low RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['Low RR'], x['Mech Vent']), axis=1)
    sumdf['RR'] = sumdf['High RR Score'].combine(sumdf['Low RR Score'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High RR', 'Low RR', 'High RR Score', 'Low RR Score'])

    sumdf['pO2 High'] = dataset.pO2High
    sumdf['pO2 Low'] = dataset.pO2Low
    sumdf['fiO2 High'] = dataset.fiO2High
    sumdf['fiO2 Low'] = dataset.fiO2Low
    sumdf['pCO2 High'] = dataset.pCO2High
    sumdf['pCO2 Low'] = dataset.pCO2Low

    sumdf['AaDO2 High Score'] = sumdf.apply(lambda x: Settings.get_aado2(x['pO2 High'], x['fiO2 High'], x['pCO2 High'], x['Mech Vent']), axis=1)
    sumdf['AaDO2 Low Score'] = sumdf.apply(lambda x: Settings.get_aado2(x['pO2 Low'], x['fiO2 Low'], x['pCO2 Low'], x['Mech Vent']), axis=1)
    sumdf['AaDO2'] = sumdf['AaDO2 High Score'].combine(sumdf['AaDO2 Low Score'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['AaDO2 High Score', 'AaDO2 Low Score', 'fiO2 High', 'fiO2 Low', 'pCO2 High'])

    sumdf['PaO2 High Score'] = sumdf.apply(lambda x: Settings.get_pao2(x['pO2 High'], x['Mech Vent']), axis=1)
    sumdf['PaO2 Low Score'] = sumdf.apply(lambda x: Settings.get_pao2(x['pO2 Low'], x['Mech Vent']), axis=1)
    sumdf['PaO2'] = sumdf['PaO2 High Score'].combine(sumdf['PaO2 Low Score'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['pO2 High', 'pO2 Low', 'Mech Vent', 'PaO2 High Score', 'PaO2 Low Score'])

    sumdf['hct lo 24h'] = dataset.hctLow
    sumdf['hct hi 24h'] = dataset.hctHigh
    sumdf['hct lo d0'] = dataset.lo_hct_d0
    sumdf['hct hi d0'] = dataset.hi_hct_d0
    sumdf['hct lo d1'] = dataset.lo_hct_d1
    sumdf['hct hi d1'] = dataset.hi_hct_d1
    sumdf['hct lo'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct lo 24h'], x['hct lo d0'], x['hct lo d1']), axis=1)
    sumdf['hct hi'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct hi 24h'], x['hct hi d0'], x['hct hi d1']), axis=1)
    sumdf['HCT'] = sumdf['hct hi'].combine(sumdf['hct lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['hct lo 24h', 'hct hi 24h', 'hct lo d0', 'hct hi d0', 'hct lo d1', 'hct hi d1', 'hct lo', 'hct hi'])

    sumdf['wbc low 24h'] = dataset.wbcLow
    sumdf['wbc high 24h'] = dataset.wbcHigh
    sumdf['wbc low d0'] = dataset.lo_wbc_d0
    sumdf['wbc high d0'] = dataset.hi_wbc_d0
    sumdf['wbc low d1'] = dataset.lo_wbc_d1
    sumdf['wbc high d1'] = dataset.hi_wbc_d1
    sumdf['wbc lo'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc low 24h'], x['wbc low d0'], x['wbc low d1']), axis=1)
    sumdf['wbc hi'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc high 24h'], x['wbc high d0'], x['wbc high d1']), axis=1)
    sumdf['WBC'] = sumdf['wbc hi'].combine(sumdf['wbc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['wbc low 24h', 'wbc high 24h', 'wbc low d0', 'wbc high d0', 'wbc low d1', 'wbc high d1', 'wbc lo', 'wbc hi'])

    sumdf['cr high'] = dataset.crHigh
    sumdf['urine'] = dataset.urineOut
    sumdf['esrd'] = dataset.esrd
    sumdf['ARF'] = sumdf.apply(lambda x: Settings.check_kidney_failure(x['cr high'], x['urine'], x['esrd']), axis=1)
    sumdf['Creatinine'] = sumdf.apply(lambda x: Settings.get_cr(x['cr high'], x['ARF']), axis=1)
    sumdf = sumdf.drop(columns=['cr high', 'urine', 'esrd', 'ARF'])

    sumdf['urine d0'] = dataset.urineOut
    sumdf['urine d1'] = dataset.urine_out_d1
    sumdf['Urine'] = sumdf.apply(lambda x: Settings.get_urine(x['urine d0'], x['urine d1']), axis=1)
    sumdf = sumdf.drop(columns=['urine d0', 'urine d1'])

    sumdf['lo urea d0'] = dataset.bunLow
    sumdf['hi urea d0'] = dataset.bunHigh
    sumdf['lo urea d1'] = dataset.lo_urea_d1
    sumdf['hi urea d1'] = dataset.hi_urea_d1
    sumdf['urea lo'] = sumdf.apply(lambda x: Settings.get_bun(x['lo urea d0'], x['lo urea d1']), axis=1)
    sumdf['urea hi'] = sumdf.apply(lambda x: Settings.get_bun(x['hi urea d0'], x['hi urea d1']), axis=1)
    sumdf['BUN'] = sumdf['urea hi'].combine(sumdf['urea lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo urea d0', 'hi urea d0', 'lo urea d1', 'hi urea d1', 'urea lo', 'urea hi'])

    temp_high['High Na'] = dataset.naHigh.apply(Settings.get_na)
    temp_low['Low Na'] = dataset.naLow.apply(Settings.get_na)
    sumdf['Serum Sodium'] = temp_high['High Na'].combine(temp_low['Low Na'], max, fill_value=0)

    sumdf['alb lo d0'] = dataset.albLow
    sumdf['alb hi d0'] = dataset.albHigh
    sumdf['alb lo d1'] = dataset.lo_alb_d1
    sumdf['alb hi d1'] = dataset.hi_alb_d1
    sumdf['alb lo'] = sumdf.apply(lambda x: Settings.get_alb(x['alb lo d0'], x['alb lo d1']), axis=1)
    sumdf['alb hi'] = sumdf.apply(lambda x: Settings.get_alb(x['alb hi d0'], x['alb hi d1']), axis=1)
    sumdf['Serum Albumin'] = sumdf['alb hi'].combine(sumdf['alb lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['alb lo d0', 'alb hi d0', 'alb lo d1', 'alb hi d1', 'alb lo', 'alb hi'])

    sumdf['bil d0'] = dataset.bilirubinLevel
    sumdf['bil d1'] = dataset.tbil_d1
    sumdf['Serum Bilirubin'] = sumdf.apply(lambda x: Settings.get_bilirubin(x['bil d0'], x['bil d1']), axis=1)
    sumdf = sumdf.drop(columns=['bil d0', 'bil d1'])

    sumdf['lo gluc d0'] = dataset.glucLow
    sumdf['hi gluc d0'] = dataset.glucHigh
    sumdf['lo gluc d1'] = dataset.lo_gluc_d1
    sumdf['hi gluc d1'] = dataset.hi_gluc_d1
    sumdf['gluc lo'] = sumdf.apply(lambda x: Settings.get_glucose(x['lo gluc d0'], x['lo gluc d1']), axis=1)
    sumdf['gluc hi'] = sumdf.apply(lambda x: Settings.get_glucose(x['hi gluc d0'], x['hi gluc d1']), axis=1)
    sumdf['Serum Glucose'] = sumdf['gluc hi'].combine(sumdf['gluc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo gluc d0', 'hi gluc d0', 'lo gluc d1', 'hi gluc d1', 'gluc lo', 'gluc hi'])

    sumdf['GCS Visual'] = dataset.comaVisual.apply(Settings.gcs_visual)
    sumdf['GCS Motor'] = dataset.comaMotor.apply(Settings.gcs_motor)
    sumdf['GCS Verbal'] = dataset.comaVerbal.apply(Settings.gcs_verbal)
    sumdf['GCS Coma'] = sumdf.apply(lambda x: Settings.gcs_combined(x['GCS Visual'], x['GCS Motor'], x['GCS Verbal']), axis=1)
    sumdf = sumdf.drop(columns=['GCS Visual', 'GCS Motor', 'GCS Verbal'])

    sumdf['ph'] = dataset.pHLow
    sumdf['pH and pCO2'] = sumdf.apply(lambda x: Settings.get_ph_pco2(x['ph'], x['pCO2 Low']), axis=1)
    sumdf = sumdf.drop(columns=['ph', 'pCO2 Low'])


    sumdf['Score'] = sumdf.sum(axis=1)
    sumdf['Study ID'] = dataset.studyID
    score = sumdf.pop('Score')
    study_id = sumdf.pop('Study ID')
    sumdf.insert(0, 'Score', score)
    sumdf.insert(0, 'Study_ID', study_id)
    Settings.exportCSV(sumdf)
    print(sumdf['Score'])
    print(sumdf)

    # PROTOYPE END