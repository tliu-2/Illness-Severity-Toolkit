import pandas as pd
import numpy as np
import math
from datetime import datetime
import Settings


def calc_o2_index(maw, fio2, pao2):
    if pao2 == -99 or np.isnan(pao2):
        return np.nan
    oi = (maw * (fio2 * 100)) / pao2
    return oi[0]


def calc_admit_discharge(admit, discharge):
    if pd.isnull(admit) or pd.isnull(discharge):
        return np.nan
    admit = datetime.strptime(admit, "%Y-%m-%d %H:%M")
    discharge = datetime.strptime(discharge, "%Y-%m-%d %H:%M")
    diff = discharge - admit
    return diff


def make_tuples(_array, slicc_id):
    tuple_list = []
    for item in _array:
        tuple_list.append((slicc_id, item))
    return tuple_list


def remove_hour_min(_datestr):
    length = len(_datestr)
    return _datestr[:length - 6]


def calc_pf(p, f):
    if p == -99 or np.isnan(p) or f == -99 or np.isnan(f):
        return np.nan
    pf = p / f
    return pf[0]


def run(df, test=False):
    df_t = df.groupby(by='slicc_subject_id', as_index=True, sort=False)
    list_dates = []
    list_oi_b1 = []
    list_oi_b2 = []
    for slicc_id, group in df_t:
        # print(f"at {slicc_id}")
        dates = group.iloc[0]
        group = group.iloc[1:, :]

        if group.empty:
            continue

        if str(dates['b1_datetime']).strip() != 'nan':
            bronch1 = remove_hour_min(dates['b1_datetime'])
            b1 = group[group['date_dly'] == bronch1]
            # print("reached b1")
            oi_b1 = calc_o2_index(b1['tx_hosp_vent_dly_maw'].values, b1['tx_hosp_vent_dly_fio2'].values,
                                  b1['lab_hosp_pao2_l_dly'].values)
            pf_b1 = calc_pf(b1['lab_hosp_pao2_l_dly'].values, b1['tx_hosp_vent_dly_fio2'].values)
            list_oi_b1.append((slicc_id, oi_b1, pf_b1))

        if str(dates['b2_datetime']).strip() != 'nan':
            bronch2 = remove_hour_min(dates['b2_datetime'])
            b2 = group[group['date_dly'] == bronch2]
            # print("reached b2")
            oi_b2 = calc_o2_index(b2['tx_hosp_vent_dly_maw'].values, b2['tx_hosp_vent_dly_fio2'].values,
                                  b2['lab_hosp_pao2_l_dly'].values)
            pf_b2 = calc_pf(b2['lab_hosp_pao2_l_dly'].values, b2['tx_hosp_vent_dly_fio2'].values)

            list_oi_b2.append((slicc_id, oi_b2, pf_b2))

        admit_discharge = calc_admit_discharge(dates['admit_date'], dates['admit_dc_dt'])
        list_dates.append((slicc_id, admit_discharge))

    b1_df = pd.DataFrame(list_oi_b1, columns=['slicc_subject_id', 'OI_B1', 'P/F_B1'])
    b2_df = pd.DataFrame(list_oi_b2, columns=['slicc_subject_id', 'OI_B2', 'P/F_B2'])
    final_df = pd.concat([b1_df, b2_df], axis=1)

    df_dates = pd.DataFrame(list_dates, columns=['slicc_study_id', 'Relative Discharge Day'])
    final_df = pd.concat([final_df, df_dates], axis=1)

    if test:
        final_df.to_csv("./SOFA_test.csv", index=True, header=True)
    else:
        return final_df


