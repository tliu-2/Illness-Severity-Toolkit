import pandas as pd

from src.injury_severity_toolkit import Settings


def run(df, test=False):
    final_df = pd.DataFrame([])

    final_df['Temp Age'] = df['subject_dob'].apply(Settings.calculate_age_from_dob)
    final_df['Age'] = final_df['Temp Age'].apply(Settings.cci_get_age_score)
    final_df = final_df.drop(columns=['Temp Age'])
    # Weight 1
    final_df['Myocardial Infarction'] = df['comorb_charlson_mi'].apply(Settings.cci_weight1)
    final_df['Congestive Heart Failure'] = df['comorb_charlson_chf'].apply(Settings.cci_weight1)
    final_df['Peripheral Vascular Disease'] = df['comorb_charlson_pvd'].apply(Settings.cci_weight1)
    final_df['Cerebrovascular Disease'] = df['comorb_charlson_cva_mild'].apply(Settings.cci_weight1)
    final_df['Dementia'] = df['comorb_charlson_dementia'].apply(Settings.cci_weight1)
    final_df['COPD'] = df['comorb_copd'].apply(Settings.cci_weight1)
    final_df['Connective Tissue Disease'] = df['comorb_charlson_ctd'].apply(Settings.cci_weight1)
    final_df['Peptic Ulcer Disease'] = df['comorb_charlson_pud'].apply(Settings.cci_weight1)
    final_df['Mild Liver Disease'] = df['comorb_charlson_liver_mild'].apply(Settings.cci_weight1)
    final_df['Diabetes'] = df['comorb_charlson_dm_mild'].apply(Settings.cci_weight1)

    # Weight 2
    final_df['Hemiplegia'] = df['comorb_charlson_hemiplegia'].apply(Settings.cci_weight2)
    final_df['Mod-Severe Renal Disease'] = df['comorb_charlson_renal_sev'].apply(Settings.cci_weight2)
    final_df['Diabetes w/ Organ Damage'] = df['comorb_charlson_dm_severe'].apply(Settings.cci_weight2)
    final_df['Tumor'] = df['comorb_charlson_tumor_no'].apply(Settings.cci_weight2)
    final_df['Lymphoma'] = df['comorb_charlson_lymphoma'].apply(Settings.cci_weight2)
    final_df['Leukemia'] = df['comorb_charlson_leukemia'].apply(Settings.cci_weight2)

    # Weight 3
    final_df['Mod-Severe Liver Disease'] = df['comorb_charlson_liver_sev'].apply(Settings.cci_weight3)

    # Weight 6
    final_df['Metastatic Tumor'] = df['comorb_charlson_tumor_mets'].apply(Settings.cci_weight6)
    final_df['AIDS'] = df['comorb_hiv'].apply(Settings.cci_weight6)

    final_df['CCI w/ Age'] = final_df.sum(axis=1, numeric_only=True)
    score_age = final_df.pop('CCI w/ Age')

    final_df['CCI'] = final_df.iloc[:, 1:].sum(axis=1, numeric_only=True)
    final_df['Study ID'] = df['slicc_subject_id']

    score = final_df.pop('CCI')
    study_id = final_df.pop('Study ID')
    final_df.insert(0, 'Score w/ Age', score_age)
    final_df.insert(0, 'Score', score)
    final_df.insert(0, 'Study_ID', study_id)

    if test:
        final_df.to_csv("./CCI_test.csv", index=False, header=True)
    else:
        return final_df