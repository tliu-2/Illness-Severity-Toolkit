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
    sumdf['Age'] = df['subject_dob'].apply(Settings.calculate_age_from_dob)
    sumdf['Age'] = sumdf['Age'].apply(Settings.get_age)
    sumdf['Cirrhosis'] = df['comorb_charlson_liver_sev'].apply(Settings.check_cirr)
    sumdf['Cancer'] = df['comorb_charlson_tumor_mets'].apply(Settings.check_cancer)
    sumdf['Leukemia'] = df['comorb_charlson_leukemia'].apply(Settings.check_leukemia)
    sumdf['Lymphoma'] = df['comorb_charlson_leukemia'].apply(Settings.check_lymphoma)

    sumdf['HIV'] = df['comorb_hiv'].apply(Settings.check_aids)
    sumdf['Immunocomprimised'] = df['comorb_immunocomp'].apply(Settings.check_immuno_sup)

    sumdf['Heart Rate High'] = df['vs_hosp24_hr_high'].apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate Low'] = df['vs_hosp24_hr_low'].apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate'] = sumdf['Heart Rate High'].combine(sumdf['Heart Rate Low'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['Heart Rate High', 'Heart Rate Low'])

    sumdf['High BP'] = df['vs_hosp24_map_high'].apply(Settings.get_bp_score)
    sumdf['Low BP'] = df['vs_hosp24_map_high'].apply(Settings.get_bp_score)
    sumdf['Blood Pressure'] = sumdf['High BP'].combine(sumdf['Low BP'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High BP', 'Low BP'])

    sumdf['High Temp'] = df['vs_hosp24_temp_high_c'].apply(Settings.get_temp_score)
    sumdf['Low Temp'] = df['vs_hosp24_temp_low_c'].apply(Settings.get_temp_score)
    sumdf['Temperature'] = sumdf['High Temp'].combine(sumdf['Low Temp'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High Temp', 'Low Temp'])

    sumdf['High RR'] = df['vs_hosp24_rr_high']
    sumdf['Low RR'] = df['vs_hosp24_rr_low']
    sumdf['Mech Vent'] = df['mv_yn']

    sumdf['High RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['High RR'], x['Mech Vent']), axis=1)
    sumdf['Low RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['Low RR'], x['Mech Vent']), axis=1)
    sumdf['RR'] = sumdf['High RR Score'].combine(sumdf['Low RR Score'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High RR', 'Low RR', 'High RR Score', 'Low RR Score', 'Mech Vent'])

    # sumdf['AA / PaO2'] = df.apply(lambda x: Settings.get_aa_or_pao2(x['aa_max_d01'], x['pao2_min']), axis=1)
    sumdf['PaO2'] = df.apply(lambda x: Settings.get_pao2(x['lab_hosp_24h_pao2_lowest'], x['mv_yn']), axis=1)
    sumdf['AA'] = df.apply(lambda x: Settings.get_aado2(x['lab_hosp_24h_pao2_lowest'], x['lab_hosp_24h_fio2_low'],
                                                        x['lab_hosp_first_paco2'], x['mv_yn']), axis=1)

    sumdf['hct lo 24h'] = df['lab_hosp_24h_hct_low']
    sumdf['hct hi 24h'] = df['lab_hosp_24h_hct_high']
    sumdf['hct lo'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct lo 24h']),
                                  axis=1)
    sumdf['hct hi'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct hi 24h']),
                                  axis=1)
    sumdf['HCT'] = sumdf['hct hi'].combine(sumdf['hct lo'], max, fill_value=0)
    sumdf = sumdf.drop(
        columns=['hct lo 24h', 'hct hi 24h', 'hct lo', 'hct hi'])

    sumdf['wbc low 24h'] = df['lab_hosp_24h_wbc_low']
    sumdf['wbc high 24h'] = df['lab_hosp_24h_wbc_high']
    sumdf['wbc lo'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc low 24h']),
                                  axis=1)
    sumdf['wbc hi'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc high 24h']),
                                  axis=1)
    sumdf['WBC'] = sumdf['wbc hi'].combine(sumdf['wbc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['wbc low 24h', 'wbc high 24h', 'wbc lo', 'wbc hi'])

    sumdf['Kidney Failure'] = df.apply(lambda x: Settings.check_kidney_failure(x['lab_hosp_cr_high'],
                                                                               x['lab_hosp_urine_out_d0'],
                                                                               x['comorb_esrd']), axis=1)
    sumdf['Urine'] = df.apply(lambda x: Settings.get_urine(x['lab_hosp_urine_out_d0']), axis=1)
    sumdf['lab_hosp_cr_high'] = df['lab_hosp_cr_high']
    sumdf['Creatinine'] = sumdf.apply(lambda x: Settings.get_cr(x['lab_hosp_cr_high'], x['Kidney Failure']), axis=1)
    sumdf = sumdf.drop(columns=['Kidney Failure', 'lab_hosp_cr_high'])

    sumdf['lo urea d0'] = df['lab_hosp_bun_low']
    sumdf['hi urea d0'] = df['lab_hosp_bun_high']
    sumdf['urea lo'] = sumdf.apply(lambda x: Settings.get_bun(x['lo urea d0']), axis=1)
    sumdf['urea hi'] = sumdf.apply(lambda x: Settings.get_bun(x['hi urea d0']), axis=1)
    sumdf['BUN'] = sumdf['urea hi'].combine(sumdf['urea lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo urea d0', 'hi urea d0', 'urea lo', 'urea hi'])

    sumdf['High Na'] = df['lab_hosp_24h_na_high'].apply(Settings.get_na)
    sumdf['Low Na'] = df['lab_hosp_24h_na_low'].apply(Settings.get_na)
    sumdf['Serum Sodium'] = sumdf['High Na'].combine(sumdf['Low Na'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High Na', 'Low Na'])

    sumdf['alb lo d0'] = df['lab_hosp_alb_low']
    sumdf['alb hi d0'] = df['lab_hosp_alb_high']
    sumdf['alb lo'] = sumdf.apply(lambda x: Settings.get_alb(x['alb lo d0']), axis=1)
    sumdf['alb hi'] = sumdf.apply(lambda x: Settings.get_alb(x['alb hi d0']), axis=1)
    sumdf['Serum Albumin'] = sumdf['alb hi'].combine(sumdf['alb lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['alb lo d0', 'alb hi d0', 'alb lo', 'alb hi'])

    sumdf['Serum Bilirubin'] = df.apply(lambda x: Settings.get_bilirubin(x['lab_hosp_first_bili']), axis=1)

    sumdf['lo gluc d0'] = df['lab_hosp_gluc_low']
    sumdf['hi gluc d0'] = df['lab_hosp_gluc_high']
    sumdf['gluc lo'] = sumdf.apply(lambda x: Settings.get_glucose(x['lo gluc d0']), axis=1)
    sumdf['gluc hi'] = sumdf.apply(lambda x: Settings.get_glucose(x['hi gluc d0']), axis=1)
    sumdf['Serum Glucose'] = sumdf['gluc hi'].combine(sumdf['gluc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo gluc d0', 'hi gluc d0', 'gluc lo', 'gluc hi'])

    sumdf['GCS Visual'] = df['vs_hosp24_gcs_low_eye'].apply(Settings.gcs_visual)
    sumdf['GCS Motor'] = df['vs_hosp24_gcs_low_motor'].apply(Settings.gcs_motor)
    sumdf['GCS Verbal'] = df['vs_hosp24_gcs_low_speech'].apply(Settings.gcs_verbal)
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

    sumdf['pH and pCO2'] = df.apply(lambda x: Settings.get_ph_pco2(x['lab_hosp_24h_ph_low'], x['lab_hosp_first_paco2']), axis=1)

    sumdf['Score'] = sumdf.sum(axis=1, numeric_only=True)
    sumdf['Study ID'] = df['slicc_subject_id']
    score = sumdf.pop('Score')
    study_id = sumdf.pop('Study ID')
    sumdf.insert(0, 'Score', score)
    sumdf.insert(0, 'Study_ID', study_id)
    exportCSV(sumdf)
    print(sumdf['Score'])
    print(sumdf)
