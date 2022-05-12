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


def run(df, test=False):
    df_t = df.groupby(by='slicc_subject_id', as_index=True, sort=False)

    list_vfds = []
    for slicc_id, group in df_t:
        curr_vfd = 0
        if 0 in group['dispo'].values:
            continue
        vent1 = group['tx_hosp_vent_dly'].apply(calculate_vfds).sum()
        vent2 = group['tx_hosp_vent_dly_2'].apply(calculate_vfds).sum()
        curr_vfd = vent1 + vent2
        list_vfds.append((slicc_id, curr_vfd))

    final_df = pd.DataFrame(list_vfds, columns=['slicc_study_id', 'VFDs'])

    if test:
        final_df.to_csv("VFDs_test.csv", index=False, header=True)
    else:
        return final_df
