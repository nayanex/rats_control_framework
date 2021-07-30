from typing import Generic, TypeVar

import pandas as pd

from src.automation.data_access_layer import unit_of_work
from src.automation.data_transfer_object.rats_controls import QueryResult
from src.utils.utils import convert_int_list_to_str

Query = TypeVar("Query")


class BaseQueries(Generic[Query]):
    """Base queries to generate Control Framework reports."""

    def __init__(self, uow: unit_of_work.SqlAlchemyUnitOfWork):
        self.uow = uow

    def _run_query(self, query_cmd: str) -> QueryResult:
        with self.uow:
            data = list(map(dict, self.uow.session.execute(query_cmd)))
            return QueryResult(data, query_cmd)

    def _read_sql_into_data_frame(self, query_cmd: str) -> QueryResult:
        with self.uow:
            df = pd.read_sql(query_cmd, con=self.uow.conn)
            return QueryResult(df, query_cmd)

    def get_calc_request_ids(self, month: int, year: int) -> QueryResult:
        query = """
SELECT R.ID 
FROM
    IPS_OWNER.PS_CALCULATION_REQUESTS R,
    IPS_OWNER.PS_CALCULATION_INPUTS I
WHERE
    I.DATA_DICTIONARY_ID = (SELECT ID FROM IPS_OWNER.PS_DATA_DICTIONARY WHERE CODE = 'SOURCE_SYSTEM') AND
    R.MDL_IMPORT_DATASET_ID = I.IMPORT_DATASET_ID AND
    TO_CHAR(R.CREATION_TIMESTAMP, 'mm-YYYY') =  '{month}-{year}' AND
    R.REP_STATUS = 'Y' AND 
    R.DESCRIPTION IS NULL AND
    STATUS NOT IN ('MAAP_FAILED', 'FAILED')
        """.format(
            month=str(month).zfill(2), year=year
        )
        results = self._run_query(query)
        results.data = [str(r["id"]) for r in results.data]
        return results

    def get_calc_requests(self, ids: list) -> QueryResult:
        query = """
SELECT 
    cr.ID AS CALCULATION_REQUEST_ID,
    cr.creation_timestamp AS RUN_DATE,
    cr.STATUS,
    cri1.VALUE AS MDM_IMPORT_DATASET_ID,
    TO_CHAR(ids.DELIVERY_TIMESTAMP,'DD MON YYYY') AS MDM_DELIVERY_DATE,
    ci1.VALUE AS DELIVERING_SYSTEM,
    ci2.VALUE AS REPORTING_PERIOD,
    cr.RUN_ID AS SMILE_RUN_ID
FROM 
    IPS_OWNER.PS_CALCULATION_REQUESTS cr,
    IPS_OWNER.PS_IMPORT_DATASETS ids,
    (SELECT IMPORT_DATASET_ID, VALUE
    FROM IPS_OWNER.PS_CALCULATION_INPUTS
    WHERE DATA_DICTIONARY_ID = (SELECT ID FROM IPS_OWNER.PS_DATA_DICTIONARY WHERE CODE = 'SOURCE_SYSTEM')) ci1,
    (SELECT IMPORT_DATASET_ID, VALUE
    FROM IPS_OWNER.PS_CALCULATION_INPUTS
    WHERE DATA_DICTIONARY_ID = (SELECT ID FROM IPS_OWNER.PS_DATA_DICTIONARY WHERE CODE = 'REPORTING_PERIOD')) ci2,
    (SELECT CALCULATION_REQUEST_ID, VALUE
    FROM IPS_OWNER.PS_CALCULATION_REQ_INPUTS
    WHERE DATA_DICTIONARY_ID = (SELECT ID FROM IPS_OWNER.PS_DATA_DICTIONARY WHERE CODE = 'mdmImportDatasetId')) cri1
WHERE cr.ID IN ({})
    AND cr.MDL_IMPORT_DATASET_ID = ci1.IMPORT_DATASET_ID
    AND cr.MDL_IMPORT_DATASET_ID = ci2.IMPORT_DATASET_ID
    AND cr.ID = cri1.CALCULATION_REQUEST_ID
    AND cri1.VALUE = ids.ID""".format(
            ",".join(ids)
        )
        return self._run_query(query)

    def get_rats_errors_per_src_system(self, src_req: dict) -> QueryResult:
        query_template = """
SELECT
    '{system_alias}' AS DELIVERY_SYSTEM,
     COUNT(CASE WHEN error_parameter LIKE '%RATS%' THEN 1 END) AS "#recs with RATS error",
     COUNT(CASE WHEN error_parameter LIKE '%RATS:LEL_SEGMENT_EMPTY%' THEN 1 END) AS "#recs with LEL_SEGMENT_EMPTY",
     COUNT(CASE WHEN error_parameter LIKE '%MAAP%' THEN 1 END) AS "#recs with MAAP error"
FROM
    ips_owner.ps_asset_results
WHERE
    CALCULATION_REQUEST_ID IN ({request_id})
    AND ips_flag = 'N'
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
            + """order by "#recs with RATS error" desc"""
        )
        return self._run_query(query)
