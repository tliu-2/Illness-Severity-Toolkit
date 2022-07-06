import pandas as pd
import numpy as np

from src.injury_severity_toolkit import oxygenation as oi


def calc_ratio(sp, f):
    if sp == -99 or np.isnan(sp) or f == -99 or np.isnan(f):
        return np.nan
    ratio = sp / f
    return ratio


def run(df, test=False):
    df_t = df.groupby(by='slicc_subject_id', as_index=True, sort=False)
    col_order = []
    frames = []
    b1 = {}
    b2 = {}
    for slicc_id, group in df_t:
        # print(f"at {slicc_id}")
        dates = group.iloc[0]
        group = group.iloc[1:, :]

        if group.empty:
            continue

        temp_df = pd.DataFrame([])

        temp_df['slicc_subject_id'] = group['slicc_subject_id']
        temp_df['date_dly'] = range(0, len(group['date_dly']), 1)

        temp_df['PF'] = group.apply(lambda x: calc_ratio(x['lab_hosp_pao2_l_dly'], x['tx_hosp_vent_dly_fio2']), axis=1)
        temp_df['SF'] = group.apply(lambda x: calc_ratio(x['lab_hosp_sao2_l_dly'], x['lab_hosp_sf_l_dly']), axis=1)

        b1[slicc_id] = dates['b1_datetime']
        b2[slicc_id] = dates['b2_datetime']
        frames.append(temp_df)

    final_df = pd.concat(frames)
    final_df = final_df.pivot_table(index='slicc_subject_id', columns='date_dly', values=['PF', 'SF'], sort=False,
                                    dropna=False)
    final_df.columns = final_df.columns.map('{0[0]}/{0[1]}'.format)  # Flatten multi-index in columns.
    b1_df = pd.DataFrame(b1.items(), columns=['slicc_subject_id', 'b1_date'])
    b2_df = pd.DataFrame(b2.items(), columns=['slicc_subject_id', 'b2_date'])
    bronch_df = b1_df.merge(b2_df, on='slicc_subject_id')

    final_df = final_df.merge(bronch_df, on='slicc_subject_id')

    if test:
        final_df.to_csv("./SOFA_test.csv", index=True, header=True)
    else:
        return final_df
