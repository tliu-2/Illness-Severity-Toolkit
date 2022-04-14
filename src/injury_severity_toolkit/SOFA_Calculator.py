import math

import numpy as np
import pandas as pd
import Settings


def get_bronch_dates(df):
    bronch_days = {}
    for date, bronch in zip(df['date_dly'], df["bronch_day_visit"]):
        if bronch == 1:
            bronch_days["V1"] = date
        if bronch == 2:
            bronch_days["V2"] = date

    if "V1" not in bronch_days:
        bronch_days["V1"] = np.NaN
    if "V2" not in bronch_days:
        bronch_days["V2"] = np.NaN

    return bronch_days


def run(df, test=False):
    frames = []
    col_order = []
    bronch_dicts = {}
    df_grouped = df.groupby(by='slicc_subject_id', as_index=True, sort=False)
    for slicc_id, group in df_grouped:  # Divide the df into groups based on subject ID and calculate score.
        print(f'at {slicc_id}')
        urine = group['lab_hosp_urine_out_d0'].iloc[0]
        group.dropna(subset=['date_dly'], inplace=True)
        if len(group) > 0:
            temp_df = pd.DataFrame([])
            temp_df['slicc_subject_id'] = group['slicc_subject_id']
            temp_df['date_dly'] = range(0, len(group['date_dly']), 1)
            temp_df['date_dly'] = 'day' + temp_df['date_dly'].astype(str)
            col_order = temp_df['date_dly']  # not efficient....
            temp_df['Respiratory'] = group.apply(lambda x: Settings.sofa_resp(x['lab_hosp_pao2_l_dly'],
                                                                              x['lab_hosp_pf_l_dly'],
                                                                              x['tx_hosp_vent_dly']), axis=1)
            temp_df['Platelets'] = group['lab_hosp_platelet_l_dly'].apply(Settings.sofa_platelets)
            temp_df['Bilirubin'] = group['lab_hosp_bili_h_dly'].apply(Settings.sofa_bilirubin)
            temp_df['Blood Pressure'] = group.apply(lambda x: Settings.sofa_bp(x['vs_hosp_map_l_dly'],
                                                                               x['tx_hosp_pressor_dose_dly']), axis=1)
            temp_df['GCS'] = group['vs_hosp_gcs_l_dly'].apply(Settings.sofa_gcs)

            temp_df['Renal'] = group.apply(lambda x: Settings.sofa_renal(x['lab_hosp_cr_h_dly'], urine), axis=1)
            sofa_score = temp_df.iloc[:, 2:].sum(axis=1)
            temp_df.insert(2, "SOFA score", sofa_score)
            temp_df['bronch_day_visit'] = group['bronch_day_visit']
            bronch_dicts[slicc_id] = get_bronch_dates(temp_df)
            frames.append(temp_df)

    final_df = pd.concat(frames)
    final_df.dropna(subset=['date_dly'], inplace=True)
    final_df = final_df.pivot_table(index='slicc_subject_id', columns='date_dly', values='SOFA score', sort=False)
    final_df = final_df.reindex(col_order, axis=1)

    bronch_df = pd.DataFrame(bronch_dicts)
    bronch_df = bronch_df.transpose()

    final_list = [final_df, bronch_df]
    to_export = pd.concat(final_list, axis=1)

    if test:
        to_export.to_csv("./SOFA_test.csv", index=True, header=True)
    else:
        Settings.sofa_export_csv(to_export)
