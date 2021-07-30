from dataclasses import dataclass
from decimal import Decimal
from typing import Generic, TypeVar

from src.automation.adapters.mixins import ValuesMixin

RequiredData = TypeVar("RequiredData")
QueryData = TypeVar("QueryData")


@dataclass
class QueryResult:
    data: Generic[QueryData] = None
    query_cmd: str = None


@dataclass
class GeneralData(Generic[RequiredData]):
    source_per_request: dict
    calculation_requests: QueryResult


@dataclass
class RatsErrorsData:
    class Type(ValuesMixin):
        RATS = "#recs with RATS error"
        LEL_SEGMENT_EMPTY = "#recs with LEL_SEGMENT_EMPTY"

    type: str
    errors_by_src_system: QueryResult


@dataclass
class Calc1GeneralData(GeneralData[RequiredData]):
    economic_scenario_projections: list
    mps_mevs: QueryResult
    alm_dataset: QueryResult
    mdm_dataset: QueryResult
    ps_properties: QueryResult
    mortgage_rates: QueryResult


@dataclass
class Rat3GeneralData(GeneralData[RequiredData], RatsErrorsData):
    recs_with_rats_error: dict
    total_provision_impact: Decimal
    rats_error_parameters: QueryResult
    principal_outstanding: QueryResult


@dataclass
class Seg3GeneralData(GeneralData[RequiredData], RatsErrorsData):
    recs_with_lel_segment_empty: dict
    assets_with_empty_lel_segment: QueryResult


@dataclass
class EYDatasetResults:
    AAHG: QueryResult = None
    MB: QueryResult = None
    SUBSINT: QueryResult = None


@dataclass
class EYDatasetIds:
    AAHG: list = None
    MB: list = None
    SUBSINT: list = None


@dataclass
class EYGeneralData(GeneralData[RequiredData]):
    ey_legend: QueryResult
    dataset_results: EYDatasetResults = EYDatasetResults()
    dataset_ids: EYDatasetIds = EYDatasetIds()
