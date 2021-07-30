from datetime import datetime

from src.automation.data_access_layer.unit_of_work import SqlAlchemyUnitOfWork
from src.reports.cal1c import Cal1cReport
from src.reports.ey import EYReport
from src.reports.rat3 import Rat3Report
from src.reports.seg3 import Seg3Report


class ControlFrameworkReports:
    def __init__(self):
        # TODO make these values configurable via run attributes
        current_date = datetime.now()
        self.month = current_date.month
        self.year = current_date.year
        self.db = SqlAlchemyUnitOfWork()

    def run(self):
        Cal1cReport(self.month, self.year, self.db).populate_evidences_pages()
        Rat3Report(self.month, self.year, self.db).populate_evidences_pages()
        Seg3Report(self.month, self.year, self.db).populate_evidences_pages()
        ey = EYReport(self.month, self.year, self.db)
        ey.populate_evidences_pages()
        ey.generate_datasets()


if __name__ == "__main__":
    fw = ControlFrameworkReports()
    fw.run()
