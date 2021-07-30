import mock
import pytest

from src.config import get_template_filepath
from src.evidences._base import BaseEvidence
from src.reports._base import BaseReport
from src.reports.cal1c import Cal1cReport


@pytest.fixture
@mock.patch.object(BaseReport, "check_requirements_initialization")
@mock.patch.object(BaseReport, "get_template_file")
@mock.patch.object(BaseEvidence, "fetch_required_data")
def report_mock(mock_get_template, mock_init, fetch_mock):
    report = BaseReport(10, 2020, mock.Mock)
    report.report_queries = mock.Mock()
    mock_get_template.return_value = True
    mock_init.return_value = True
    fetch_mock.return_value = True
    evidence_mock = mock.Mock(spec=BaseEvidence)
    evidence_mock.__name__ = "evidence_whatever"
    report.evidences = [evidence_mock]
    report.save_output = mock.Mock()  # Do not save results
    return report


class TestReports:
    def test_run_report(self, report_mock):
        report = report_mock
        report_mock.populate_evidences_pages()
        evidence_mock = report.evidences[0]()
        evidence_mock.get_values.assert_called()
        evidence_mock.update_worksheet_with_values.assert_called_once()

    @mock.patch("src.reports._base.load_workbook")
    def test_get_template_file(self, wb_mock):
        chosen_template = get_template_filepath("CAL#1c")
        cal1c = Cal1cReport(10, 2020, mock.Mock)
        cal1c.get_template_file = mock.MagicMock(return_value=True)
        wb_mock.assert_called_with(chosen_template)
