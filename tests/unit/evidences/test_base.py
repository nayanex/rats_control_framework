import mock
import pytest

from src.automation.data_access_layer.base_queries import BaseQueries
from src.automation.data_transfer_object.rats_controls import (
    GeneralData,
    QueryResult,
)
from src.evidences._base import BaseEvidence


class TestBaseEvidence:
    @pytest.fixture(autouse=True)
    def evidence_data(self):
        valid_query = QueryResult(query_cmd="valid_query", data=["valid_ids"])
        empty_general_data = GeneralData

        yield {"empty": empty_general_data, "valid_query": valid_query}

    @mock.patch.object(BaseEvidence, "fetch_required_data")
    def test_init(self, fetch_mock):
        attrs = {"return_value": True, "other.side_effect": KeyError}
        fetch_mock.configure_mock(**attrs)
        evidence = BaseEvidence(10, 2020, mock.Mock, {"base": mock.Mock}, mock.Mock)

        assert evidence.month == 10
        assert evidence.year == 2020
        assert evidence.quarter == 4

    @mock.patch("src.evidences._base.create_dict_list_from_tuple_props")
    @mock.patch("src.evidences._base.remap_dict_list")
    @mock.patch("src.evidences._base.merge_list_of_dictionaries")
    def test_validate_general_data(
        self,
        mock_merge_list_of_dictionaries,
        mock_remap_dict_list,
        mock_create_dict_list_from_tuple_props,
        evidence_data,
    ):
        mock_create_dict_list_from_tuple_props.return_value = True
        mock_remap_dict_list.return_value = True
        mock_merge_list_of_dictionaries.return_value = True

        query = BaseQueries(mock.Mock)
        query.get_calc_request_ids = mock.MagicMock(
            return_value=evidence_data["valid_query"]
        )
        query.get_calc_requests = mock.MagicMock(
            return_value=evidence_data["valid_query"]
        )

        BaseEvidence(10, 2020, evidence_data["empty"], {"base": mock.Mock}, query)
        query.get_calc_requests.assert_called_with(["valid_ids"])
