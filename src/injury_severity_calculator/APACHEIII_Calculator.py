# This program calculates the APACHE score of a patients on using their Day 0 statistics.
# How it works:
# This program functions by taking an entire column of patient data in a .csv file and assigns all the measurements
# in the column to its respective APACHE score for that individual measurement. (using panda Series)
# This data is then placed into a Pandas' database. The program then utilizes the dataframe.sum(axis) method
# (axis = 1) such that the row values are summed (total score for an individual).

import pandas as pd
import Settings as Settings

def run(df):
    sumdf = pd.DataFrame([])

    sumdf['Age'] = df['age'].apply(Settings.get_age)
    sumdf['Cirrhosis'] = df['comorb_cirr'].apply(Settings.check_cirr)
    sumdf['Cancer'] = df['comorb_cancer'].apply(Settings.check_cancer)
    sumdf['Leukemia'] = df['comorb_leukemia'].apply(Settings.check_leukemia)
    sumdf['Lymphoma'] = df['comorb_leukemia'].apply(Settings.check_lymphoma)

    sumdf['AIDS'] = df['comorb_aids'].apply(Settings.check_aids)
    sumdf['Immunocomprimised'] = df['comorb_immunocomp'].apply(Settings.check_immuno_sup)

    sumdf['Heart Rate High'] = df['hr_max_d01'].apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate Low'] = df['hr_min_d01'].apply(Settings.get_heart_rate_score)
    sumdf['Heart Rate'] = sumdf['Heart Rate High'].combine(sumdf['Heart Rate Low'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['Heart Rate High', 'Heart Rate Low'])

    sumdf['High BP'] = df['map_max_d01'].apply(Settings.get_bp_score)
    sumdf['Low BP'] = df['map_min_d01'].apply(Settings.get_bp_score)
    sumdf['Blood Pressure'] = sumdf['High BP'].combine(sumdf['Low BP'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High BP', 'Low BP'])

    sumdf['High Temp'] = df['temp_max_d01'].apply(Settings.get_temp_score)
    sumdf['Low Temp'] = df['temp_min_d01'].apply(Settings.get_temp_score)
    sumdf['Temperature'] = sumdf['High Temp'].combine(sumdf['Low Temp'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High Temp', 'Low Temp'])

    sumdf['High RR'] = df['rr_max_d01']
    sumdf['Low RR'] = df['rr_min_d01']
    sumdf['Mech Vent'] = df['highestrespsupport_d01']

    sumdf['High RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['High RR'], x['Mech Vent']), axis=1)
    sumdf['Low RR Score'] = sumdf.apply(lambda x: Settings.get_rr_score(x['Low RR'], x['Mech Vent']), axis=1)
    sumdf['RR'] = sumdf['High RR Score'].combine(sumdf['Low RR Score'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High RR', 'Low RR', 'High RR Score', 'Low RR Score'])


    sumdf['AA / PaO2'] = df.apply(lambda x: Settings.get_aa_or_pao2(x['aa_max_d01'], x['pao2_min']), axis=1)


    sumdf['hct lo 24h'] = df['hct_max_d01']
    sumdf['hct hi 24h'] = df['hct_min_d01']
    sumdf['hct lo'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct lo 24h']),
                                  axis=1)
    sumdf['hct hi'] = sumdf.apply(lambda x: Settings.get_hematocrit(x['hct hi 24h']),
                                  axis=1)
    sumdf['HCT'] = sumdf['hct hi'].combine(sumdf['hct lo'], max, fill_value=0)
    sumdf = sumdf.drop(
        columns=['hct lo 24h', 'hct hi 24h', 'hct lo', 'hct hi'])

    sumdf['wbc low 24h'] = df['wbc_max_d01']
    sumdf['wbc high 24h'] = df['wbc_min_d01']
    sumdf['wbc lo'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc low 24h']),
                                  axis=1)
    sumdf['wbc hi'] = sumdf.apply(lambda x: Settings.get_wbc(x['wbc high 24h']),
                                  axis=1)
    sumdf['WBC'] = sumdf['wbc hi'].combine(sumdf['wbc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['wbc low 24h', 'wbc high 24h', 'wbc lo', 'wbc hi'])

    # Creatinine score slightly different due to removal of urine
    # sumdf['cr high'] = df['cr_max_d01']
    # sumdf['urine'] = df['aki']
    # sumdf['aki'] = df['esrd']
    # sumdf['ARF'] = sumdf.apply(lambda x: Settings.check_kidney_failure(x['cr high'], x['urine'], x['esrd']), axis=1)
    # sumdf['Creatinine'] = sumdf.apply(lambda x: Settings.get_cr(x['cr high'], x['ARF']), axis=1)
    # sumdf = sumdf.drop(columns=['cr high', 'urine', 'esrd', 'ARF'])

    sumdf['Creatinine'] = df.apply(lambda x: Settings.get_cr(x['cr_max_d01'], x['aki']), axis=1)

    # Urine not accounted for in this version
    # sumdf['urine d0'] = df['urine_out_d0']
    # sumdf['urine d1'] = df['urine_out_d1']
    # sumdf['Urine'] = sumdf.apply(lambda x: Settings.get_urine(x['urine d0'], x['urine d1']), axis=1)
    # sumdf = sumdf.drop(columns=['urine d0', 'urine d1'])

    sumdf['lo urea d0'] = df['urea_max_d01']
    sumdf['hi urea d0'] = df['urea_min_d01']
    sumdf['urea lo'] = sumdf.apply(lambda x: Settings.get_bun(x['lo urea d0']), axis=1)
    sumdf['urea hi'] = sumdf.apply(lambda x: Settings.get_bun(x['hi urea d0']), axis=1)
    sumdf['BUN'] = sumdf['urea hi'].combine(sumdf['urea lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo urea d0', 'hi urea d0', 'urea lo', 'urea hi'])

    sumdf['High Na'] = df['na_max_d01'].apply(Settings.get_na)
    sumdf['Low Na'] = df['na_min_d01'].apply(Settings.get_na)
    sumdf['Serum Sodium'] = sumdf['High Na'].combine(sumdf['Low Na'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['High Na', 'Low Na'])

    sumdf['alb lo d0'] = df['alb_max_d01']
    sumdf['alb hi d0'] = df['alb_min_d01']
    sumdf['alb lo'] = sumdf.apply(lambda x: Settings.get_alb(x['alb lo d0']), axis=1)
    sumdf['alb hi'] = sumdf.apply(lambda x: Settings.get_alb(x['alb hi d0']), axis=1)
    sumdf['Serum Albumin'] = sumdf['alb hi'].combine(sumdf['alb lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['alb lo d0', 'alb hi d0', 'alb lo', 'alb hi'])

    sumdf['Serum Bilirubin'] = df.apply(lambda x: Settings.get_bilirubin(x['tbili_max_d01']), axis=1)

    sumdf['lo gluc d0'] = df['gluc_max_d01']
    sumdf['hi gluc d0'] = df['gluc_min_d01']
    sumdf['gluc lo'] = sumdf.apply(lambda x: Settings.get_glucose(x['lo gluc d0']), axis=1)
    sumdf['gluc hi'] = sumdf.apply(lambda x: Settings.get_glucose(x['hi gluc d0']), axis=1)
    sumdf['Serum Glucose'] = sumdf['gluc hi'].combine(sumdf['gluc lo'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['lo gluc d0', 'hi gluc d0', 'gluc lo', 'gluc hi'])

    sumdf['GCS Visual'] = df['lo_gcs_visual_d01'].apply(Settings.gcs_visual)
    sumdf['GCS Motor'] = df['lo_gcs_motor_d01'].apply(Settings.gcs_motor)
    sumdf['GCS Verbal'] = df['lo_gcs_verbal_d01'].apply(Settings.gcs_verbal)
    sumdf['GCS Coma'] = sumdf.apply(lambda x: Settings.gcs_combined(x['GCS Visual'], x['GCS Motor'], x['GCS Verbal']),
                                    axis=1)
    sumdf = sumdf.drop(columns=['GCS Visual', 'GCS Motor', 'GCS Verbal'])

    sumdf['ph'] = df['ph_min_d01']
    sumdf['pCO2 min'] = df['pco2_phmin_d01']
    sumdf['pCO2 max'] = df['pco2_phmax_d01']
    sumdf['ph_pco2_min'] = sumdf.apply(lambda x: Settings.get_ph_pco2(x['ph'], x['pCO2 min']), axis=1)
    sumdf['ph_pco2_max'] = sumdf.apply(lambda x: Settings.get_ph_pco2(x['ph'], x['pCO2 max']), axis=1)
    sumdf['pH and pCO2'] = sumdf['ph_pco2_max'].combine(sumdf['ph_pco2_min'], max, fill_value=0)
    sumdf = sumdf.drop(columns=['ph', 'pCO2 min', 'pCO2 max', 'ph_pco2_min', 'ph_pco2_max'])

    sumdf['Score'] = sumdf.sum(axis=1, numeric_only=True)
    sumdf['Study ID'] = df['study_id']
    score = sumdf.pop('Score')
    study_id = sumdf.pop('Study ID')
    sumdf.insert(0, 'Score', score)
    sumdf.insert(0, 'Study_ID', study_id)

    Settings.export_csv(sumdf)
    print(sumdf['Score'])
    print(sumdf)
