import pandas as pd

import Settings


def calculate_vfds(row):
    """
    Calculates VFDs based on intubation variables.
    :param row: A row from the csv file as a Pandas Series with dead_date and 28day_dead1_alive0 removed.
    :return: Total # of VFDs
    """
    if row == 0:
        return 1
    else:
        return 0

def run(df):
    df_t = df.groupby(by='slicc_subject_id', as_index=True, sort=False)

    list_vfds = list()
    for slicc_id, group in df_t:
        curr_vfd = 0
        if 0 in group['dispo'].values:
            continue
        vent1 = group['tx_hosp_vent_dly'].apply(calculate_vfds).sum()
        vent2 = group['tx_hosp_vent_dly_2'].apply(calculate_vfds).sum()
        curr_vfd = vent1 + vent2
        list_vfds.append((slicc_id, curr_vfd))

    df_final = pd.DataFrame(list_vfds, columns=['slicc_study_id', 'VFDs'])
    Settings.export_csv(df_final)