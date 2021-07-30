import mock
import pytest

from src.main import ControlFrameworkReports


@pytest.mark.freeze_time("2020-10-10")
@mock.patch("src.main.SqlAlchemyUnitOfWork")
class TestControlFrameworkReports:
    def test_init(self, _):
        fw = ControlFrameworkReports()
        assert fw.month == 10
        assert fw.year == 2020

    @mock.patch("src.main.Cal1cReport")
    @mock.patch("src.main.Rat3Report")
    @mock.patch("src.main.Seg3Report")
    @mock.patch("src.main.EYReport")
    def test_run(self, sql_mock, rat3_mock, calc1_mock, seg3_mock, ey_mock):
        fw = ControlFrameworkReports()
        fw.run()
        sql_mock.assert_called()
        calc1_mock.assert_called()
        rat3_mock.assert_called()
        seg3_mock.assert_called()
        ey_mock.assert_called()
