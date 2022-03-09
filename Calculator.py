# This program calculates the APACHE score of a patients on using their Day 0 statistics.
# How it works:
# This program functions by taking an entire column of patient data in a .csv file and assigns all the measurements
# in the column to its respective APACHE score for that individual measurement. (using panda Series)
# This data is then placed into a Pandas' database. The program then utilizes the dataframe.sum(axis) method
# (axis = 1) such that the row values are summed (total score for an individual).

import pandas as pd
import Settings as Settings

from tkinter import filedialog


def exportCSV(df):
    exportfile = filedialog.asksaveasfilename(defaultextension='.csv')
    df.to_csv(exportfile, index=None, header=True)


def run(df):
    sumdf = pd.DataFrame([])
    sumdf['Age'] = df['age'].apply(Settings.get_age)
    sumdf['Cirrhosis'] = df['cirr'].apply(Settings.check_cirr)
    sumdf['Cancer'] = df['cancer'].apply(Settings.check_cancer)
    #sumdf['Leukemia'] = df['comorb_charlson_leukemia'].apply(Settings.check_leukemia)
    #sumdf['Lymphoma'] = df['comorb_charlson_leukemia'].apply(Settings.check_lymphoma)

    #sumdf['HIV'] = df['comorb_hiv'].apply(Settings.check_aids)
    sumdf['Immunocomprimised'] = df['immunodef'].apply(Settings.check_immuno_sup)

    sumdf['Heart Rate High'] = df['hi_hr_d0'].apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate Low'] = df['lo_hr_d0'].apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate'] = sumdf['Heart Rate High'].combine(sumdf['Heart Rate Low'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['Heart Rate High', 'Heart Rate Low'])

    sumdf['High BP'] = df['hi_map_d0'].apply(Settings.get_bp_score)
    sumdf['Low BP'] = df['lo_map_d0'].apply(Settings.get_bp_score)
    sumdf['Blood Pressure'] = sumdf['High BP'].combine(sumdf['Low BP'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High BP', 'Low BP'])

    sumdf['High Temp'] = df['hi_temp_d0'].apply(Settings.get_temp_score)
    sumdf['Low Temp'] = df['lo_temp_d0'].apply(Settings.get_temp_score)
    sumdf['Temperature'] = sumdf['High Temp'].combine(sumdf['Low Temp'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High Temp', 'Low Temp'])

    sumdf['High RR'] = df['hi_rr_d0']
    sumdf['Low RR'] = df['lo_rr_d0']
    sumdf['Mech Vent'] = df['mv_day_of_bronch']

    sumdf['High RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['High RR'], x['Mech Vent']), axis=1)
    sumdf['Low RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['Low RR'], x['Mech Vent']), axis=1)
    sumdf['RR'] = sumdf['High RR Score'].combine(sumdf['Low RR Score'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High RR', 'Low RR', 'High RR Score', 'Low RR Score', 'Mech Vent'])

    # sumdf['AA / PaO2'] = df.apply(lambda x: Settings.get_aa_or_pao2(x['aa_max_d01'], x['pao2_min']), axis=1)
    sumdf['High_PaO2'] = df.apply(lambda x: Settings.get_pao2(x['lo_po2_d0'], x['mv_day_of_bronch']), axis=1)
    sumdf['Low_PaO2'] = df.apply(lambda x: Settings.get_pao2(x['hi_po2_d0'], x['mv_day_of_bronch']), axis=1)
    sumdf['PaO2'] = sumdf['High_PaO2'].combine(sumdf['Low_PaO2'], max, fill_value=0)
    sumdf['Low_AA'] = df.apply(lambda x: Settings.get_aado2(x['lo_po2_d0'], x['abg_lo_fi02_d0'],
                                                        x['ph_lo_co2_d0'], x['mv_day_of_bronch']), axis=1)
    sumdf['High_AA'] = df.apply(lambda x: Settings.get_aado2(x['hi_po2_d0'], x['abg_hi_fi02_d0'],
                                                             x['ph_hi_co2_d0'], x['mv_day_of_bronch']), axis=1)
    sumdf['AA'] = sumdf['High_AA'].combine(sumdf['Low_AA'], max, fill_value=0)
    sumdf = sumdf.drop(
        columns=['High_PaO2', 'Low_PaO2', 'Low_AA', 'High_AA']
    )

    sumdf['hct lo 24h'] = df['lo_hct_d0']
    sumdf['hct hi 24h'] = df['hi_hct_d0']
    sumdf['hct lo'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct lo 24h']),
                                  axis=1)
    sumdf['hct hi'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct hi 24h']),
                                  axis=1)
    sumdf['HCT'] = sumdf['hct hi'].combine(sumdf['hct lo'], max, fill_value=0)
    sumdf = sumdf.drop(
        columns=['hct lo 24h', 'hct hi 24h', 'hct lo', 'hct hi'])

    sumdf['wbc low 24h'] = df['lo_wbc_d0']
    sumdf['wbc high 24h'] = df['hi_wbc_d0']
    sumdf['wbc lo'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc low 24h']),
                                  axis=1)
    sumdf['wbc hi'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc high 24h']),
                                  axis=1)
    sumdf['WBC'] = sumdf['wbc hi'].combine(sumdf['wbc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['wbc low 24h', 'wbc high 24h', 'wbc lo', 'wbc hi'])

    sumdf['Kidney Failure'] = df.apply(lambda x: Settings.check_kidney_failure(x['hi_cr_d0'],
                                                                               x['out_d0'],
                                                                               x['esrd']), axis=1)
    sumdf['Urine'] = df.apply(lambda x: Settings.get_urine(x['out_d0']), axis=1)
    sumdf['lab_hosp_cr_high'] = df['hi_cr_d0']
    sumdf['Creatinine'] = sumdf.apply(lambda x: Settings.get_cr(x['lab_hosp_cr_high'], x['Kidney Failure']), axis=1)
    sumdf = sumdf.drop(columns=['Kidney Failure', 'lab_hosp_cr_high'])

    sumdf['lo urea d0'] = df['lo_bun_d0']
    sumdf['hi urea d0'] = df['hi_bun_d0']
    sumdf['urea lo'] = sumdf.apply(lambda x: Settings.get_bun(x['lo urea d0']), axis=1)
    sumdf['urea hi'] = sumdf.apply(lambda x: Settings.get_bun(x['hi urea d0']), axis=1)
    sumdf['BUN'] = sumdf['urea hi'].combine(sumdf['urea lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo urea d0', 'hi urea d0', 'urea lo', 'urea hi'])

    sumdf['High Na'] = df['hi_na_d0'].apply(Settings.get_na)
    sumdf['Low Na'] = df['lo_na_d0'].apply(Settings.get_na)
    sumdf['Serum Sodium'] = sumdf['High Na'].combine(sumdf['Low Na'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High Na', 'Low Na'])

    sumdf['alb lo d0'] = df['lo_alb_d0']
    sumdf['alb hi d0'] = df['hi_alb_d0']
    sumdf['alb lo'] = sumdf.apply(lambda x: Settings.get_alb(x['alb lo d0']), axis=1)
    sumdf['alb hi'] = sumdf.apply(lambda x: Settings.get_alb(x['alb hi d0']), axis=1)
    sumdf['Serum Albumin'] = sumdf['alb hi'].combine(sumdf['alb lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['alb lo d0', 'alb hi d0', 'alb lo', 'alb hi'])

    sumdf['Serum Bilirubin'] = df.apply(lambda x: Settings.get_bilirubin(x['tbil_d0']), axis=1)

    sumdf['lo gluc d0'] = df['lo_glu_d0']
    sumdf['hi gluc d0'] = df['hi_glu_d0']
    sumdf['gluc lo'] = sumdf.apply(lambda x: Settings.get_glucose(x['lo gluc d0']), axis=1)
    sumdf['gluc hi'] = sumdf.apply(lambda x: Settings.get_glucose(x['hi gluc d0']), axis=1)
    sumdf['Serum Glucose'] = sumdf['gluc hi'].combine(sumdf['gluc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo gluc d0', 'hi gluc d0', 'gluc lo', 'gluc hi'])

    sumdf['GCS Visual'] = df['lo_gcs_visual_d0'].apply(Settings.gcs_visual)
    sumdf['GCS Motor'] = df['lo_gcs_motor_d0'].apply(Settings.gcs_motor)
    sumdf['GCS Verbal'] = df['lo_gcs_verbal_d0'].apply(Settings.gcs_verbal)
    sumdf['GCS Coma'] = sumdf.apply(lambda x: Settings.gcs_combined(x['GCS Visual'], x['GCS Motor'], x['GCS Verbal']),
                                    axis=1)
    sumdf = sumdf.drop(columns=['GCS Visual', 'GCS Motor', 'GCS Verbal'])

    # SLICC's ph, pco2 is different
    # sumdf['ph'] = df['lab_hosp_24h_ph_low']
    # sumdf['pCO2 min'] = df['pco2_phmin_d01']
    # sumdf['pCO2 max'] = df['pco2_phmax_d01']
    # sumdf['ph_pco2_min'] = sumdf.apply(lambda x: Settings.get_ph_pco2(x['ph'], x['pCO2 min']), axis=1)
    # sumdf['ph_pco2_max'] = sumdf.apply(lambda x: Settings.get_ph_pco2(x['ph'], x['pCO2 max']), axis=1)
    # sumdf['pH and pCO2'] = sumdf['ph_pco2_max'].combine(sumdf['ph_pco2_min'], max, fill_value=0)
    # sumdf = sumdf.drop(columns=['ph', 'pCO2 min', 'pCO2 max', 'ph_pco2_min', 'ph_pco2_max'])

    sumdf['pH and pCO2'] = df.apply(lambda x: Settings.get_ph_pco2(x['lo_ph_d0'], x['ph_lo_co2_d0']), axis=1)

    sumdf['Score'] = sumdf.sum(axis=1, numeric_only=True)
    sumdf['Study ID'] = df['study_id']
    score = sumdf.pop('Score')
    study_id = sumdf.pop('Study ID')
    sumdf.insert(0, 'Score', score)
    sumdf.insert(0, 'Study_ID', study_id)
    exportCSV(sumdf)
    print(sumdf['Score'])
    print(sumdf)
