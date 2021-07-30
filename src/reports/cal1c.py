from src.automation.data_access_layer.cal1c_queries import Calc1cQueries
from src.automation.data_transfer_object.rats_controls import Calc1GeneralData
from src.evidences.cal1c.evidence_b import EvidenceB
from src.evidences.cal1c.evidence_c import EvidenceC
from src.evidences.cal1c.evidence_d import EvidenceD
from src.evidences.cal1c.evidence_e import EvidenceE
from src.reports._base import BaseReport


class Cal1cReport(BaseReport):
    FILENAME = "CAL#1c"
    report_type = BaseReport.ReportType.QUARTERLY
    evidences = [EvidenceB, EvidenceC, EvidenceD, EvidenceE]
    report_queries = Calc1cQueries
    general_data = Calc1GeneralData
