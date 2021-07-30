from src.automation.data_access_layer.base_queries import BaseQueries, Query
from src.automation.data_transfer_object.rats_controls import QueryResult


class Calc1cQueries(BaseQueries[Query]):
    def get_import_datasets(self, month: int, year: int) -> QueryResult:
        data_import_type_id = 8
        status = "FINISHED"
        query = """
SELECT 
    d.id,d.delivery_timestamp, d.status, d.progress_message, d.data_import_type_id, i.description
FROM IPS_OWNER.ps_import_datasets d
LEFT JOIN IPS_OWNER.ps_data_import_types i ON i.id = d.data_import_type_id
WHERE DATA_IMPORT_TYPE_ID={type_id} AND STATUS='{status}' AND
    to_char(d.delivery_timestamp, 'mm-YYYY') >= '{month}-{year}'
ORDER BY d.delivery_timestamp DESC
FETCH FIRST 1 ROW ONLY
        """.format(
            type_id=data_import_type_id,
            status=status,
            month=str(month).zfill(2),
            year=year,
        )
        return self._run_query(query)

    def get_mevs(
        self, calc_id: int, quarter: int, year: int, codes: list
    ) -> QueryResult:
        query = """
SELECT mev.IMPORT_DATASET_ID, sc.NAME, mev.YEAR, mev.QUARTER, dd.CODE, mev.VALUE
FROM
    IPS_OWNER.rs_macro_economic_variables mev,
    IPS_OWNER.ps_data_dictionary dd,
    IPS_OWNER.rs_calculation_scenarios sc
WHERE mev.import_dataset_id = {calc_id}
    AND dd.ID = mev.DATA_DICTIONARY_ID
    AND mev.CALCULATION_SCENARIO_ID = sc.ID
    AND mev.YEAR = {year}
    AND mev.QUARTER = {quarter}
    AND sc.NAME = 'Baseline'
    AND dd.CODE IN ('{codes}')
""".format(
            calc_id=calc_id, year=year, quarter=quarter, codes="', '".join(codes)
        )
        return self._run_query(query)

    def get_scenario_weights(self) -> QueryResult:
        query = """
SELECT 
T.PROPERTY_NAME,
T.PROPERTY_VALUE,
T.DESCRIPTION 
FROM IPS_OWNER.PS_PROPERTIES T 
WHERE T.PROPERTY_NAME LIKE 'RATS_SCENARIO_WEIGHT%'        
"""
        return self._run_query(query)

    def get_alm_import_dataset(self) -> QueryResult:
        query = """
SELECT * 
FROM IPS_OWNER.PS_IMPORT_DATASETS 
WHERE DATA_IMPORT_TYPE_ID=11 AND status='FINISHED' 
ORDER BY id DESC    
FETCH FIRST 1 ROW ONLY
"""
        return self._run_query(query)

    def get_mortgage_rates(
        self,
        dataset_id: int,
        year: int,
    ) -> QueryResult:
        query = """
SELECT mev.IMPORT_DATASET_ID, sc.NAME, mev.YEAR, mev.MONTH, mev.QUARTER, dd.CODE, mev.VALUE
FROM 
    IPS_OWNER.rs_macro_economic_variables mev,
    IPS_OWNER.ps_data_dictionary dd,
    IPS_OWNER.rs_calculation_scenarios sc
WHERE mev.import_dataset_id = {dataset_id}
    AND dd.ID = mev.DATA_DICTIONARY_ID
    AND mev.CALCULATION_SCENARIO_ID = sc.ID
    AND mev.YEAR >= {year}
    AND code = 'AAB_MORTGAGE_RATE_10Y'
ORDER BY 1,2,3,4,5     
""".format(
            dataset_id=dataset_id, year=year
        )
        return self._run_query(query)
