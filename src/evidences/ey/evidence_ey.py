from src.evidences._base import BaseEvidence
from src.utils.logger import CustomLogger
from src.utils.utils import filter_dict_list_by_props

logger = CustomLogger(__name__).get_logger()


class EvidencesEY(BaseEvidence):
    worksheet_name = "Legend CALC IDs"

    def get_values(self):
        """
        Get all required data from DB.
        """
        self.values = self.general_data

        self.values.ey_legend.data = filter_dict_list_by_props(
            self.general_data.calculation_requests.data,
            "calculation_request_id",
            "delivering_system",
            "run_date",
            "reporting_period",
        )

        self.values.ey_legend.query_cmd = self.values.calculation_requests.query_cmd
        self._get_ids_per_dataset_type()
        self._extract_ey_data()

    def _get_ids_per_dataset_type(self):
        """
        Get IDs related to specific dataset type.
        """
        self.values.dataset_ids.AAHG = self.values.source_per_request.pop("AAH")
        self.values.dataset_ids.MB = self.values.source_per_request.pop("Main Bank")
        self.values.dataset_ids.SUBSINT = [
            item
            for sublist in self.values.source_per_request.values()
            for item in sublist
        ]

    def update_worksheet_with_values(self):
        """
        Provide received date to worksheet as evidences.
        """
        if self.values.ey_legend.data:
            self._print_ey_legend()
        else:
            logger.exception(
                "Extraction method did not find EY Data for any delivery system."
            )

    def _print_ey_legend(self):
        ey_legend = self.values.ey_legend
        self.add_query_and_result(self.ws["A1"], ey_legend, dict_params={})

    def fetch_required_data(self):
        super().fetch_required_data()
        self.general_data.ey_legend = self.general_data.calculation_requests

    def _extract_ey_data(self):
        """
        Extract EY data from MPS database for dataset types AAHG, MB and SubsInt.
        """
        logger.info("Extracting AAHG data.")
        self.values.dataset_results.AAHG = self.query.get_ey_dataset(
            self.values.dataset_ids.AAHG
        )
        logger.info("Successfully extracted AAHG data.")

        logger.info("Extracting Main Bank data.")
        self.values.dataset_results.MB = self.query.get_ey_dataset(
            self.values.dataset_ids.MB
        )
        logger.info("Successfully extracted Main Bank data.")

        logger.info("Extracting SubsInt data.")
        self.values.dataset_results.SUBSINT = self.query.get_ey_dataset(
            self.values.dataset_ids.SUBSINT
        )
        logger.info("Successfully extracted SubsInt data.")
