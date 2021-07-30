from src.automation.data_access_layer.base_queries import BaseQueries, Query
from src.automation.data_transfer_object.rats_controls import QueryResult
from src.utils.utils import convert_int_list_to_str


class Rat3Queries(BaseQueries[Query]):
    def get_rats_error_parameters(self, src_req: dict) -> QueryResult:
        query_template = """
SELECT
    '{system_alias}' AS DELIVERY_SYSTEM,
    error_parameter,
    Count(*) AS "#recs with RATS/MAAP error"
FROM
    ips_owner.ps_asset_results
WHERE
    calculation_request_id IN ({request_id})
    AND ips_flag = 'N'
    AND (error_parameter LIKE '%RATS%' OR error_parameter LIKE '%MAAP%')
GROUP BY
    error_parameter
"""
        query = (
            "UNION ".join(
                [
                    query_template.format(
                        system_alias=alias,
                        request_id=convert_int_list_to_str(src_req[alias]),
                    )
                    for alias in src_req.keys()
                ]
            )
            + """order by "#recs with RATS/MAAP error" desc"""
        )
        return self._run_query(query)

    def get_rats_principal_outstanding(self, src_req: dict) -> QueryResult:
        query_template = """
SELECT
    '{system_alias}' AS DELIVERY_SYSTEM,
    lubsl3.business_segment_lvl_3_descr AS bsl3,
    a.effective_stage_id,
    Count(*) AS "#recs with RATS/MAAP error", 
    SUM(b.principal_outstanding)
FROM
    ips_owner.ps_asset_results a,
    ips_owner.ps_assets b,
    ips_owner.ps_lu_business_segment_lvl_3 lubsl3
WHERE
    calculation_request_id IN ({request_id})
    AND ips_flag = 'N'
    AND (
        (error_parameter LIKE '%RATS%' OR error_parameter LIKE '%MAAP%')
        AND error_parameter NOT LIKE '%RATS:LEL_SEGMENT_EMPTY%'
    )
    AND b.id = a.asset_id
    AND b.segment_level_3_code = lubsl3.business_segment_lvl_3_key (+)
GROUP BY
    lubsl3.business_segment_lvl_3_descr,
    a.effective_stage_id
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

    def get_provision_sum_after_adjustment(self, src_req: dict) -> QueryResult:
        query_template = """
SELECT
    '{system_alias}' AS DELIVERY_SYSTEM,
    lubsl3.business_segment_lvl_3_descr AS bsl3,
    a.effective_stage_id,
    SUM(b.principal_outstanding) AS "Sum of Principal Outstanding",
    SUM(effective_provision) AS "Sum of Provision After Adjustment"
FROM
    ips_owner.ps_asset_results a,
    ips_owner.ps_assets b,
    ips_owner.ps_lu_business_segment_lvl_3 lubsl3
WHERE
    calculation_request_id IN ({request_id})
    AND ips_flag = 'N'
    AND (
        error_parameter IS NULL
        OR error_parameter NOT LIKE '%RATS%'
        OR error_parameter NOT LIKE '%MAAP%'
    )
    AND b.id = a.asset_id
    AND b.segment_level_3_code = lubsl3.business_segment_lvl_3_key (+)
GROUP BY
    lubsl3.business_segment_lvl_3_descr,
    a.effective_stage_id
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
