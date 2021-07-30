import mock
import pytest

from src.automation.data_access_layer.cal1c_queries import Calc1cQueries
from src.automation.data_transfer_object.rats_controls import QueryResult


@pytest.fixture(autouse=True)
def query_calc_req_ids():
    yield QueryResult(query_cmd="valid_query", data=[9734, 9730, 9658, 9655])


@pytest.fixture(autouse=True)
def calc1_query(sqlite_uow_factory):
    uow = sqlite_uow_factory
    query = Calc1cQueries(uow)
    yield query


class TestEvidenceB:
    @mock.patch.object(Calc1cQueries, "get_calc_request_ids")
    def test_correct_cal_requests_are_collected(
        self, mock_calc_req, calc1_query, query_calc_req_ids
    ):
        mock_calc_req.return_value = query_calc_req_ids
        out = calc1_query.get_calc_request_ids(9, 2020).data
        mock_calc_req.assert_called_with(9, 2020)
        assert out == [9734, 9730, 9658, 9655]

    def test_calc_requests_used_most_recent_quarterly_finished_mdm_import_dataset(self):
        """ "For every cal_request_id_queried_check_MDM_DELIVERY_DATE_is the most_recent and MDM_IMPORT_DATA_SET is 1549
        status is finished and DATA_IMPORT_TYPE_ID = 8 (Quarterly MEV import via MDM)
        """
        pass
