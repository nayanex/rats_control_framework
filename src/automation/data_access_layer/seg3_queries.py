from src.automation.data_access_layer.base_queries import BaseQueries, Query
from src.automation.data_transfer_object.rats_controls import QueryResult
from src.utils.utils import convert_int_list_to_str


class Seg3Queries(BaseQueries[Query]):
    def get_ps_asset_results_per_src_sys_with_empty_lel_segment(
        self, src_req: dict
    ) -> QueryResult:
        query_template = """
SELECT '{system_alias}' AS DELIVERY_SYSTEM, 
    a.local_facility_id, a.credit_agreement_id, a.REPORTING_ENTITY_CODE, 
    a.EXPOSURE_ID, b.effective_stage_id, b.RISK_STAGE_IDENTIFIER, a.claim,
    b.EFFECTIVE_PROVISION, a.COLLATERAL_VALUE_AT_SNAPSHOT, 
    a.PROGRAM_LENDING_FLAG, a.MORTGAGE_PORTFOLIO, a.CREDIT_PRODUCT_PROGRAM,
    a.NHG_FLAG, a.SEGMENT_LEVEL_3_CODE, a.OBLIGOR_CLIENT_SEGMENT
FROM ips_owner.ps_asset_results b,
     ips_owner.ps_assets a
WHERE a.id = b.asset_id AND
      b.CALCULATION_REQUEST_ID IN ({request_id}) AND
      ips_flag = 'N' AND
      ERROR_PARAMETER LIKE '%RATS:LEL_SEGMENT_EMPTY%'
"""
        query = "UNION ".join(
            [
                query_template.format(
                    system_alias=alias,
                    request_id=convert_int_list_to_str(src_req[alias]),
                )
                for alias in src_req.keys()
            ]
        )
        return self._run_query(query)
