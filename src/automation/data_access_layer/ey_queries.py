from src.automation.data_access_layer.base_queries import BaseQueries, Query
from src.automation.data_transfer_object.rats_controls import QueryResult
from src.utils.utils import convert_int_list_to_str


class EYQueries(BaseQueries[Query]):
    def get_ey_dataset(self, ids: list) -> QueryResult:
        query = """
select
a.ID,
a.RISK_STAGE_IDENTIFIER,
b.SSF_FP_ARRANGEMENT_IDENTIFIER,
a.LPD_DETERIORATION_FLAG,
c.asset_result_id,
a.CALCULATION_REQUEST_ID,
b.PROGRAM_LENDING_FLAG,
b.SEGMENT_LEVEL_3_CODE,
b.CREDIT_PRODUCT_PROGRAM,
b.OBLIGOR_CLIENT_SEGMENT,
b.OBLIGOR_UCR_CURRENT,
b.MONTHS_IN_DEFAULT,
b.PREVIOUS_MODEL_CODE_SCOR_PL,
b.PREVIOUS_FINE_CRG,
b.LATEST_MODEL_CODE_SCOR_PL,
b.FINE_CRG,
b.PREVIOUS_PERFORMANCE_IND,
b.LATEST_PERFORMANCE_IND,
b.PRINCIPAL_OUTSTANDING,
b.ARREARS_AMOUNT,
b.ALLOCATED_CREDIT_LIMIT,
b.PROGRAM_LENDING_POOL_ID,
b.COLLATERAL_VALUE_AT_SNAPSHOT,
b.COLLATERAL_TYPE,
b.DRAWN_INDICATOR,
b.CONTRACTUAL_INTEREST_RATE,
b.REPAYMENT_SCHEDULE_TYPE,
b.SETTLEMENT_DATE,
b.MORTGAGE_PORTFOLIO,
b.NHG_FLAG,
b.MONTHS_PAST_DUE,
b.ORIGINAL_PRINCIPAL_AMOUNT,
b.MATURITY_DATE,
b.COLLATERAL_ORIGINAL_VALUE,
b.FACILITY_START_DATE,
b.REVOLVING_INDICATOR,
b.PROBABILITY_OF_DEFAULT,
b.original_pd,
a.EFFECTIVE_STAGE_ID,
b.ssf_cf_arrangement_identifier,
b.LOCAL_FACILITY_ID,
b.EXPOSURE_ID,
b.REPORTING_ENTITY_CODE,
a.EFFECTIVE_PROVISION,
b.PRODUCT_TYPE,
a.WATCH_STATUS,
b.WATCHLIST_FLAG,
b.FORBORN_FLAG,
a.IPS_FLAG,
a.PORTFOLIO_CODE,
a.IFRS9CR_IMP_PERIOD_ENDDT,
a.IFRS9CR_IMP_PERIOD_STARTDT,
b.PAST_DUE_FLAG,
a.ORIGINAL_LIFETIME_PD,
a.RESIDUAL_LIFETIME_PD,
b.DEFAULT_INDICATOR,
b.OBLIGOR_UCR_AT_START,
a.ORIGINAL_EFFECTIVE_STAGE_ID,
b.OBLIGOR_ID,
case when b.principal_outstanding > 3000000 then b.OBLIGOR_NAME else null end as obligor_name,
b.CREDIT_AGREEMENT_ID,
b.GLOBAL_FACILITY_ID,
b.RESULT_OBLIGOR_ID,
b.MAIN_BORROWER_ID,
a.CALCULATED_STAGE1_PROVISION,
a.CALCULATED_STAGE2_PROVISION,
a.CALCULATED_STAGE3_PROVISION,
a.client_segment_lel,
b.CIF_IMPAIRED_STATUS,
b.OBLIGOR_AGIC,
b.claim,
b.Resultant_EAD,
b.TTC_LGD_PERC_WITHOUT_CONS,
b.TTC_PD_PERC_WITHOUT_CONS,
c.expected_loss_weighted_avg,
c.prob_of_loss_weighted_avg,
c.loss_given_loss_weighted_avg,
c.exposure_at_loss_avg,
c.discount_factor,
c.expected_loss_base_scenario,
c.prob_of_loss_base_scenario,
c.loss_given_loss_base_scenario,
c.expected_loss_neg_scenario,
c.prob_of_loss_neg_scenario,
c.loss_given_loss_neg_scenario,
c.expected_loss_pos_scenario,
c.prob_of_loss_pos_scenario,
c.loss_given_loss_pos_scenario,
c.exposure_at_loss_base_scenario,
c.exposure_at_loss_neg_scenario,
c.exposure_at_loss_pos_scenario,
b.COLL_MARKET_VAL_AT_SNAPSHOT,
b.COLL_MARKET_ORIGINAL_VALUE
from ips_owner.PS_ASSET_RESULTS a,
     ips_owner.PS_ASSETS b,
     ips_owner.PS_LU_REPORTING_UNIT lur,
     ips_owner.ps_asset_stage_results c,
     ips_owner.PS_LU_BUSINESS_SEGMENT_LVL_3 lubsl3
where a.CALCULATION_REQUEST_ID in ({request_ids})
and ips_flag = 'N'
and REPORTING_ENTITY_CODE = lur.REPORTING_UNIT_KEY (+)
and SEGMENT_LEVEL_3_CODE = lubsl3.BUSINESS_SEGMENT_LVL_3_KEY (+)
and a.ID = c.asset_result_id (+)
and a.effective_stage_ID = c.stage_ID (+)
and b.ID = a.ASSET_ID
""".format(
            request_ids=convert_int_list_to_str(ids)
        )
        return self._run_query(query)
