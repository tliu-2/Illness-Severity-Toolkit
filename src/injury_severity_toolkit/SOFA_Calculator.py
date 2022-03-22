import pandas as pd

import Settings


def run(df, test=False):

    frames = []
    df_grouped = df.groupby(by='slicc_subject_id', as_index=True, sort=False)
    for slicc_id, group in df_grouped:
        temp_df = pd.DataFrame([])
        temp_df['slicc_subject_id'] = group['slicc_subject_id']
        temp_df['Date'] = group['date_dly']
        temp_df['Respiratory'] = group.apply(lambda x: Settings.sofa_resp(x['lab_hosp_pao2_l_dly'],
                                                                          x['lab_hosp_pf_l_dly'],
                                                                          x['tx_hosp_vent_dly']), axis=1)
        temp_df['Platelets'] = group['lab_hosp_platelet_l_dly'].apply(Settings.sofa_platelets)
        temp_df['Bilirubin'] = group['lab_hosp_bili_h_dly'].apply(Settings.sofa_bilirubin)
        temp_df['Blood Pressure'] = group.apply(lambda x: Settings.sofa_bp(x['vs_hosp_map_l_dly'],
                                                         x['tx_hosp_pressor_dose_dly']), axis=1)
        temp_df['GCS'] = group['vs_hosp_gcs_l_dly'].apply(Settings.sofa_gcs)

        urine = group['lab_hosp_urine_out_d0'].iloc[0]
        temp_df['Renal'] = group.apply(lambda x: Settings.sofa_renal(x['lab_hosp_cr_h_dly'], urine), axis=1)
        sofa_score = temp_df.iloc[:, 2:].sum(axis=1)
        temp_df.insert(1, "SOFA score", sofa_score)
        frames.append(temp_df)

    final_df = pd.concat(frames)

    if test:
        final_df.to_csv("./tests/SOFA_Test.csv", index=False, header=True)
    else:
        Settings.export_csv(final_df)
