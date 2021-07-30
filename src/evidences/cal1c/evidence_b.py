from src.evidences._base import BaseEvidence
from src.utils.logger import CustomLogger
from src.utils.utils import get_month_year_as_string

logger = CustomLogger(__name__).get_logger()


class EvidenceB(BaseEvidence):
    worksheet_name = "evidence B"

    def get_values(self):
        """
        Get all required data from DB.
        """
        self.values = self.general_data

    def update_worksheet_with_values(self):
        """
        Provide received date to worksheet as evidences.
        """
        if self.values.mdm_dataset.data:
            self._print_mdm_data_id()
            self._print_calc_requests()
        else:
            logger.exception("No MDM data IDs retrieved from query.")

    def _print_mdm_data_id(self):
        mdm = self.values.mdm_dataset
        self.ws["B45"] = (
            "By query result below the status of MDM file with ID {} is  FINISHED and delivery_timestamp is the most "
            "recent date, it means that we are using this MDM table for the runs.".format(
                mdm.data[0]["id"]
            )
        )
        self.ws["B46"] = (
            "In the query result below the delivery timestamp is {date}. "
            "All the runs are done after {date}".format(
                date=str(mdm.data[0]["delivery_timestamp"])[:10]
            )
        )
        self.add_query_and_result(
            self.ws["B48"], mdm, dict_params={"bold_columns": ["id"]}
        )

    def _print_calc_requests(self):
        calc_req = self.values.calculation_requests
        date = str(self.values.mdm_dataset.data[0]["delivery_timestamp"])[:10]
        self.ws[
            "B13"
        ] = "Below query on the CORE database production environment (see results) proves that the run "
        self.ws[
            "B14"
        ] = "over reporting period {month}-{year} used MDM data delivered on {date}".format(
            month=self.month, year=self.year, date=date
        )
        self.add_query_and_result(
            self.ws["B16"],
            calc_req,
            dict_params={
                "bold_columns": ["mdm_import_dataset_id", "mdm_delivery_date"]
            },
        )
        first_calc = calc_req.data[0]
        self.ws[
            "B38"
        ] = "Calculation request ID {calc_id} is created for entity {entity}.".format(
            calc_id=first_calc["calculation_request_id"],
            entity=first_calc["delivering_system"],
        )

        self.ws[
            "B39"
        ] = "The run started at {calc_date} and used the latest MDM table which is imported at {date} with ID {id}.".format(
            calc_date=first_calc["run_date"].strftime("%d-%m-%Y"),
            id=self.values.mdm_dataset.data[0]["id"],
            date=date,
        )

        self.ws[
            "B40"
        ] = "In the Output #1 it is visible that for all the runs in {month} the MDM {id} is used which is imported \
         at {date}".format(
            month=get_month_year_as_string(self.month, self.year, "%B %Y"),
            id=self.values.mdm_dataset.data[0]["id"],
            date=date,
        )

    def fetch_required_data(self):
        super().fetch_required_data()
        self.general_data.mdm_dataset = self.query.get_import_datasets(
            self.month, self.year
        )
