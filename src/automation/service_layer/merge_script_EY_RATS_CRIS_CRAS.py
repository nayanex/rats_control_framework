import pathlib
from os import path

import pandas as pd

PROJECT_ROOT = pathlib.Path(__file__).parent.absolute()

# specify dirs
cras_dir = path.join(PROJECT_ROOT, "CRAS")
cris_dir = path.join(PROJECT_ROOT, "CRIS")
rats_dir = path.join(PROJECT_ROOT, "RATS_DATA")
vienna_dir = path.join(PROJECT_ROOT, "VIENNA")

# set up file names
cris_file_dir = path.join(cris_dir, "CRISEY2021Q1.csv")
cras_file_dir = path.join(cras_dir, "CRASEY2021Q1.xlsx")
cris_columns_dir = path.join(cris_dir, "column_names.csv")
rats_dir_aahg = path.join(rats_dir, "Q1_2021_AAHG_dataset.csv")
lpd_db_extract = path.join(vienna_dir, "March-LPD-2021.csv")
vienna_file_dir = path.join(vienna_dir, "vienna.xlsx")


# read cris
cris_columns_df = pd.read_csv(cris_columns_dir, delimiter=",")
cris = pd.read_csv(cris_file_dir, delimiter=",", names=cris_columns_df.columns)
cris = cris.rename(
    columns={
        "RSD_ID": "RISK_STAGE_IDENTIFIER",
        "OUTOFDEFAULT_PROBATION": "OUT_OF_DEFAULT_PROBATION",
    }
)

# read cras
cras = pd.read_excel(cras_file_dir, index_col=None)
cras = cras.rename(
    columns={
        "FORBEARANCE_ MEASURE": "FORBEARANCE_MEASURE",
        "PAST DUE DATE": "PAST_DUE_DATE",
        "OUTOFDEFAULT PROBATION": "OUT_OF_DEFAULT_PROBATION",
        "WATCH LIST": "WATCH_LIST",
        "DEFAULT TRIGGER": "DEFAULT_TRIGGER",
        "DAYS PAST THRESHOLD": "DAYS_PAST_THRESHOLD",
    }
)
cras = cras.drop(columns=["COUNTERPARTY"])

cris.columns
cras.columns

# concat cris cras
concat_set = pd.concat([cras, cris], axis=0, ignore_index=True)
concat_set["RISK_STAGE_IDENTIFIER"].nunique()

# read rats sets
rats_dir_main = path.join(rats_dir, "Q1_2021_MB_dataset.csv")
rats_dir_int = path.join(rats_dir, "Q1_2021_SUBSINT_dataset.csv")

rats_main_df = pd.read_csv(rats_dir_main, delimiter="|", encoding="ISO-8859-1")
rats_main_df.columns = map(str.upper, rats_main_df.columns)
rats_int_df = pd.read_csv(rats_dir_int, delimiter="|", encoding="ISO-8859-1")
rats_int_df.columns = map(str.upper, rats_int_df.columns)

# merge criscras + rats
merged_main = pd.merge(rats_main_df, concat_set, how="left", on="RISK_STAGE_IDENTIFIER")
merged_main["RISK_STAGE_IDENTIFIER"].nunique()
merged_int = pd.merge(rats_int_df, concat_set, how="left", on="RISK_STAGE_IDENTIFIER")

merged_int.count()
merged_main.count()

merged_main_head = merged_main.head(1000)
merged_main_head.drop_duplicates()

# save to csv
print("Saving merge result to CSV files")
merged_int.to_csv("SUBS_INT_rats_cris_cras_set2.csv", index=False, sep=",", decimal=".")
merged_main.to_csv(
    "MAIN_BANK_rats_cris_cras_set2.csv", index=False, sep=",", decimal="."
)

# -----------MERGE VIENNA, AAHG & LPD -------------


# read aahg and lpd data
aahg_set = pd.read_csv(rats_dir_aahg, delimiter="|", encoding="ISO-8859-1")
aahg_set.columns = map(str.upper, rats_int_df.columns)

df_lpd_db = pd.read_csv(lpd_db_extract, delimiter=",")
df_lpd_db = df_lpd_db.filter(["LPDR", "LPDO", "LPD_CF_ID"])

# merge lpd with aahg
merged_lpd = pd.merge(
    aahg_set,
    df_lpd_db,
    how="left",
    left_on="SSF_FP_ARRANGEMENT_IDENTIFIER",
    right_on="LPD_CF_ID",
)
merged_lpd = merged_lpd.drop(columns=["LPD_CF_ID"])
merged_lpd = merged_lpd.drop_duplicates()

# read vienna data
vienna = pd.read_excel(vienna_file_dir, index_col=None)

# merge vienna data with merged aahg data
merged_vienna = pd.merge(
    merged_lpd,
    vienna,
    how="left",
    left_on="SSF_FP_ARRANGEMENT_IDENTIFIER",
    right_on="FP_ARRANGEMENTIDENTIFIER",
)
merged_vienna.count()
merged_vienna = merged_vienna.drop(columns=["FP_ARRANGEMENTIDENTIFIER"])

# save to csv
print("Saving Mortgage merge result as CSV files")
merged_lpd.to_csv("Mortgages_LPD_Data_Q4_EY.csv", index=False, sep=",", decimal=".")
