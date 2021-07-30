import numpy as np
import pandas as pd


def compute_outstanding_impact(principal_outstanding, provision_sum_after_adjustment):
    df_impact = pd.DataFrame(principal_outstanding)
    df_prov_after_adj = pd.DataFrame(provision_sum_after_adjustment)

    df_prov_after_adj["Flat rates (cov ratio)"] = df_prov_after_adj[
        "Sum of Provision After Adjustment"
    ] / df_prov_after_adj["Sum of Principal Outstanding"].replace(0, np.nan)

    common_columns = ["delivery_system", "bsl3", "effective_stage_id"]
    new_df = pd.merge(df_impact, df_prov_after_adj, on=common_columns, how="left")

    new_df["Applied Flat rates"] = (
        new_df["Flat rates (cov ratio)"] * new_df["SUM(B.PRINCIPAL_OUTSTANDING)"]
    )

    return new_df.to_dict("records")
