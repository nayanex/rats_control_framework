import pytest

from src.automation.adapters.delivery_system_map import DELIVERY_SYSTEM_MAP
from src.utils.utils import (
    convert_int_list_to_str,
    create_dict_list_from_tuple_props,
    filter_dict_list_by_props,
    get_last_months_of_upcoming_quarters,
    get_month_year_as_string,
    get_previous_quarter,
    get_quarter_from_month,
    get_scenario_name,
    merge_list_of_dictionaries,
    remap_dict_list,
)


class TestUtils:
    @pytest.mark.parametrize(
        "month,quarter",
        [
            (1, 1),
            (2, 1),
            (3, 1),
            (4, 2),
            (5, 2),
            (6, 2),
            (7, 3),
            (8, 3),
            (9, 3),
            (10, 4),
            (11, 4),
            (12, 4),
        ],
    )
    def test_get_quarter_from_month(self, month, quarter):
        assert get_quarter_from_month(month) == quarter

    @pytest.mark.parametrize("quarter,result", [(1, 4), (2, 1), (3, 2), (4, 3)])
    def test_get_previous_quarter(self, quarter, result):
        assert get_previous_quarter(quarter) == result

    @pytest.mark.parametrize(
        "quarter,result",
        [
            (1, {(2020, 3), (2020, 6), (2020, 9), (2020, 12)}),
            (2, {(2020, 6), (2020, 9), (2020, 12), (2021, 3)}),
            (3, {(2020, 9), (2020, 12), (2021, 3), (2021, 6)}),
            (4, {(2020, 12), (2021, 3), (2021, 6), (2021, 9)}),
        ],
    )
    def test_get_last_months_of_upcoming_quarters(self, quarter, result):
        assert (
            get_last_months_of_upcoming_quarters(quarter, year=2020, number=4) == result
        )

    @pytest.mark.parametrize(
        "month,year,str_format,result",
        [(9, 2019, "%B %Y", "September 2019"), (10, 2020, "%b %Y", "Oct 2020")],
    )
    def test_get_month_year_as_string(self, month, year, str_format, result):
        assert get_month_year_as_string(month, year, str_format) == result

    def test_convert_int_list_to_str(self):
        test_list = [1, 2, 3]
        assert convert_int_list_to_str(test_list) == "1, 2, 3"

    def test_get_scenario_name(self):
        out = get_scenario_name(3, 2020)
        assert out == "AUG 2020 BASE"


class TestDictionariesUtils:
    @pytest.fixture(autouse=True)
    def dic_test_lists(self):
        raw = [
            {"id": 9634, "system": "IHUB-HK2", "status": "REP_DONE"},
            {"id": 9643, "system": "VIENNA", "status": "REP_DONE"},
            {"id": 9622, "system": "BRDWH", "status": "REP_DONE"},
            {"id": 9625, "system": "IHUB-CN1", "status": "REP_DONE"},
            {"id": 9628, "system": "IHUB-SG1", "status": "REP_DONE"},
        ]
        filtered = [
            {"IHUB-HK2": 9634},
            {"VIENNA": 9643},
            {"BRDWH": 9622},
            {"IHUB-CN1": 9625},
            {"IHUB-SG1": 9628},
        ]
        yield {"raw": raw, "filtered": filtered}

    def test_filter_dict_list_by_props(self, dic_test_lists):
        out = filter_dict_list_by_props(dic_test_lists["raw"], "system", "status")
        assert out == [
            {"system": "IHUB-HK2", "status": "REP_DONE"},
            {"system": "VIENNA", "status": "REP_DONE"},
            {"system": "BRDWH", "status": "REP_DONE"},
            {"system": "IHUB-CN1", "status": "REP_DONE"},
            {"system": "IHUB-SG1", "status": "REP_DONE"},
        ]

    def test_create_dict_list_from_tuple_props(self, dic_test_lists):
        out = create_dict_list_from_tuple_props(dic_test_lists["raw"], "system", "id")
        assert out == dic_test_lists["filtered"]

    def test_remap_dict_list(self, dic_test_lists):
        out = remap_dict_list(dic_test_lists["filtered"], DELIVERY_SYSTEM_MAP)
        assert out == [
            {"HongKong": 9634},
            {"AAH": 9643},
            {"Brazil": 9622},
            {"China": 9625},
            {"Singapore": 9628},
        ]

    def test_merge_list_of_dictionaries(self, dic_test_lists):
        out = merge_list_of_dictionaries(dic_test_lists["raw"])
        assert out == {
            "id": [9634, 9643, 9622, 9625, 9628],
            "status": ["REP_DONE", "REP_DONE", "REP_DONE", "REP_DONE", "REP_DONE"],
            "system": ["IHUB-HK2", "VIENNA", "BRDWH", "IHUB-CN1", "IHUB-SG1"],
        }
