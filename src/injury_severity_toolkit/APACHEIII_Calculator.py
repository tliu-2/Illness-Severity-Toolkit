# This program calculates the APACHE score of a patients on using their Day 0 statistics.
# How it works:
# This program functions by taking an entire column of patient data in a .csv file and assigns all the measurements
# in the column to its respective APACHE score for that individual measurement. (using panda Series)
# This data is then placed into a Pandas' database. The program then utilizes the dataframe.sum(axis) method
# (axis = 1) such that the row values are summed (total score for an individual).

import pandas as pd
import Settings as Settings


def run(df, test=False):
    sumdf = pd.DataFrame([])
    df['Temp Age'] = df['subject_dob'].apply(Settings.calculate_age_from_dob)
    sumdf['Age'] = df['Temp Age'].apply(Settings.get_age)

    sumdf['Cirrhosis'] = df['comorb_charlson_liver_sev'].apply(Settings.check_cirr)
    sumdf['Cancer'] = df['comorb_charlson_tumor_mets'].apply(Settings.check_cancer)
    sumdf['Leukemia'] = df['comorb_charlson_leukemia'].apply(Settings.check_leukemia)
    sumdf['Lymphoma'] = df['comorb_charlson_lymphoma'].apply(Settings.check_lymphoma)

    sumdf['AIDS'] = df['comorb_hiv'].apply(Settings.check_aids)
    sumdf['Immunocomprimised'] = df['comorb_immunocomp'].apply(Settings.check_immuno_sup)

    df['Heart Rate High'] = df['vs_hosp24_hr_high'].apply(Settings.get_heart_rate_score)
    df['Heart Rate Low'] = df['vs_hosp24_hr_low'].apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate'] = df['Heart Rate High'].combine(df['Heart Rate Low'], max, fill_value=0)

    df['High BP'] = df['vs_hosp24_map_high'].apply(Settings.get_bp_score)
    df['Low BP'] = df['vs_hosp24_map_low'].apply(Settings.get_bp_score)
    sumdf['Blood Pressure'] = df['High BP'].combine(df['Low BP'], max, fill_value=0)

    df['High Temp'] = df['vs_hosp24_temp_high_c'].apply(Settings.get_temp_score)
    df['Low Temp'] = df['vs_hosp24_temp_low_c'].apply(Settings.get_temp_score)
    sumdf['Temperature'] = df['High Temp'].combine(df['Low Temp'], max, fill_value=0)

    df['High RR Score'] = df.apply(lambda x: Settings.get_rr_score(x['vs_hosp24_rr_high'], x['mv_yn']), axis=1)
    df['Low RR Score'] = df.apply(lambda x: Settings.get_rr_score(x['vs_hosp24_rr_low'], x['mv_yn']), axis=1)
    sumdf['RR'] = df['High RR Score'].combine(df['Low RR Score'], max, fill_value=0)

    sumdf['AA / PaO2'] = df.apply(lambda x: Settings.get_aado2(x['lab_hosp_24h_pao2_lowest'],
                                                               x['lab_hosp_24h_fio2_low'],
                                                               x['lab_hosp_first_paco2'],
                                                               x['mv_yn']), axis=1)

    # sumdf['AA / PaO2'] = df.apply(lambda x: Settings.get_aa_or_pao2(x['aa_max_d01'], x['pao2_min']), axis=1)

    df['hct lo'] = df.apply(lambda x: Settings.get_hematocrit(x['lab_hosp_24h_hct_low']),
                            axis=1)
    df['hct hi'] = df.apply(lambda x: Settings.get_hematocrit(x['lab_hosp_24h_hct_high']),
                            axis=1)
    sumdf['HCT'] = df['hct hi'].combine(df['hct lo'], max, fill_value=0)

    df['wbc lo'] = df.apply(lambda x: Settings.get_wbc(x['lab_hosp_24h_wbc_low']),
                            axis=1)
    df['wbc hi'] = df.apply(lambda x: Settings.get_wbc(x['lab_hosp_24h_wbc_high']),
                            axis=1)
    sumdf['WBC'] = df['wbc hi'].combine(df['wbc lo'], max, fill_value=0)

    # Creatinine score slightly different due to removal of urine
    # sumdf['cr high'] = df['cr_max_d01']
    # sumdf['urine'] = df['aki']
    # sumdf['aki'] = df['esrd']
    # sumdf['ARF'] = sumdf.apply(lambda x: Settings.check_kidney_failure(x['cr high'], x['urine'], x['esrd']), axis=1)
    # sumdf['Creatinine'] = sumdf.apply(lambda x: Settings.get_cr(x['cr high'], x['ARF']), axis=1)
    # sumdf = sumdf.drop(columns=['cr high', 'urine', 'esrd', 'ARF'])

    df['ARF'] = df.apply(lambda x: Settings.check_kidney_failure(x['lab_hosp_cr_high'],
                                                                 x['lab_hosp_urine_out_d0'],
                                                                 x['comorb_esrd']), axis=1)
    sumdf['Creatinine'] = df.apply(lambda x: Settings.get_cr(x['lab_hosp_cr_high'], x['ARF']), axis=1)

    # Urine not accounted for in this version
    # sumdf['urine d0'] = df['urine_out_d0']
    # sumdf['urine d1'] = df['urine_out_d1']
    # sumdf['Urine'] = sumdf.apply(lambda x: Settings.get_urine(x['urine d0'], x['urine d1']), axis=1)
    # sumdf = sumdf.drop(columns=['urine d0', 'urine d1'])

    sumdf['Urine'] = df['lab_hosp_urine_out_d0'].apply(Settings.get_urine)

    df['urea lo'] = df.apply(lambda x: Settings.get_bun(x['lab_hosp_bun_low']), axis=1)
    df['urea hi'] = df.apply(lambda x: Settings.get_bun(x['lab_hosp_bun_high']), axis=1)
    sumdf['BUN'] = df['urea hi'].combine(df['urea lo'], max, fill_value=0)

    df['High Na'] = df['lab_hosp_24h_na_high'].apply(Settings.get_na)
    df['Low Na'] = df['lab_hosp_24h_na_low'].apply(Settings.get_na)
    sumdf['Serum Sodium'] = df['High Na'].combine(df['Low Na'], max, fill_value=0)

    df['alb lo'] = df.apply(lambda x: Settings.get_alb(x['lab_hosp_alb_low']), axis=1)
    df['alb hi'] = df.apply(lambda x: Settings.get_alb(x['lab_hosp_alb_high']), axis=1)
    sumdf['Serum Albumin'] = df['alb hi'].combine(df['alb lo'], max, fill_value=0)

    sumdf['Serum Bilirubin'] = df.apply(lambda x: Settings.get_bilirubin(x['lab_hosp_first_bili']), axis=1)

    df['gluc lo'] = df.apply(lambda x: Settings.get_glucose(x['lab_hosp_gluc_low']), axis=1)
    df['gluc hi'] = df.apply(lambda x: Settings.get_glucose(x['lab_hosp_gluc_high']), axis=1)
    sumdf['Serum Glucose'] = df['gluc hi'].combine(df['gluc lo'], max, fill_value=0)

    df['GCS Visual'] = df['vs_hosp24_gcs_low_eye'].apply(Settings.gcs_visual)
    df['GCS Motor'] = df['vs_hosp24_gcs_low_motor'].apply(Settings.gcs_motor)
    df['GCS Verbal'] = df['vs_hosp24_gcs_low_speech'].apply(Settings.gcs_verbal)
    sumdf['GCS Coma'] = df.apply(lambda x: Settings.gcs_combined(x['GCS Visual'], x['GCS Motor'], x['GCS Verbal']),
                                 axis=1)

    sumdf['pH and pCO2'] = df.apply(lambda x: Settings.get_ph_pco2(x['lab_hosp_24h_ph_low'], x['lab_hosp_first_paco2']),
                                    axis=1)

    sumdf['Score'] = sumdf.sum(axis=1, numeric_only=True)
    sumdf['Study ID'] = df['slicc_subject_id']
    score = sumdf.pop('Score')
    study_id = sumdf.pop('Study ID')
    sumdf.insert(0, 'Score', score)
    sumdf.insert(0, 'Study_ID', study_id)

    if test:
        sumdf.to_csv("./tests/APACHE_Test.csv", index=False, header=True)
    else:
        Settings.export_csv(sumdf)
