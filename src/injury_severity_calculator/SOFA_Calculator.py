import pandas as pd

import Settings


def run(df):
    final_df = pd.DataFrame([])

    final_df['Respiratory'] = df.apply(lambda x: Settings.sofa_resp(x['lab_hosp_pao2_l_dly'],
                                                                    x['lab_hosp_pf_l_dly'],
                                                                    x['mv_yn']))
    final_df['Platelets'] = df['lab_hosp_platelet_l_dly'].apply(Settings.sofa_platelets)
    final_df['Bilirubin'] = df['lab_hosp_bili_h_dly'].apply(Settings.sofa_bilirubin)
    final_df['Blood Pressure'] = df.apply(lambda x: Settings.sofa_bp(x['vs_hosp_map_l_dly'],
                                                                     x['tx_hosp_pressor_dose_dly']))
    final_df['GCS'] = df['vs_hosp_gcs_l_dly'].apply(lambda x: Settings.sofa_gcs)
    final_df['Renal'] = df.apply(lambda x: Settings.sofa_renal(x['lab_hosp_cr_h_dly'],
                                                               x['lab_hosp_urine_out_d0']))

    final_df['SOFA Score'] = final_df.sum(axis=1, numeric_only=True)
    final_df['Study_ID'] = df['slicc_subject_id']

    score = final_df.pop('SOFA Score')
    study_id = final_df.pop('Study_ID')
    final_df.insert(0, 'SOFA Score', score)
    final_df.insert(0, 'Study_ID', study_id)

    Settings.export_csv(final_df)
