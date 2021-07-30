from src.automation.data_access_layer.rat3_queries import Rat3Queries
from src.automation.data_transfer_object.rats_controls import Rat3GeneralData
from src.evidences.rat3.evidence_a import EvidenceA
from src.evidences.rat3.evidence_b import EvidenceB
from src.reports._base import BaseReport


class Rat3Report(BaseReport):
    FILENAME = "RAT#3"
    report_type = BaseReport.ReportType.QUARTERLY
    evidences = [EvidenceA, EvidenceB]
    report_queries = Rat3Queries
    general_data = Rat3GeneralData
