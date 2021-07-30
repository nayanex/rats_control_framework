from src.automation.data_access_layer.seg3_queries import Seg3Queries
from src.automation.data_transfer_object.rats_controls import Seg3GeneralData
from src.evidences.seg3.evidence_a import EvidenceA
from src.evidences.seg3.evidence_b import EvidenceB
from src.reports._base import BaseReport


class Seg3Report(BaseReport):
    FILENAME = "SEG#3"
    report_type = BaseReport.ReportType.QUARTERLY
    evidences = [EvidenceA, EvidenceB]
    report_queries = Seg3Queries
    general_data = Seg3GeneralData
