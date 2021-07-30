from src.automation.data_transfer_object.rats_controls import RatsErrorsData
from src.automation.service_layer.rats_errors import (
    get_only_records_with_specific_error,
)
from src.evidences._base import BaseEvidence
from src.utils.logger import CustomLogger

logger = CustomLogger(__name__).get_logger()


class EvidenceA(BaseEvidence):
    worksheet_name = "evidence A"

    def get_values(self):
        """
        Get all required data from DB.
        """
        self.values = self.general_data

    def update_worksheet_with_values(self):
        """
        Provide received date to worksheet as evidences.
        """
        if self.values.errors_by_src_system.data:
            self._print_errors_by_src_system()
        else:
            logger.exception("No rats error found for any delivery system.")

    def _print_errors_by_src_system(self):
        rats_errors = self.values.errors_by_src_system
        self.add_query_and_result(self.ws["B14"], rats_errors, dict_params={})
        self.ws["B39"] = "RATS errors for {}.".format(
            ", ".join(self.values.recs_with_rats_error.keys())
        )

    def fetch_required_data(self):
        super().fetch_required_data()

        self.general_data.errors_by_src_system = (
            self.query.get_rats_errors_per_src_system(
                self.general_data.source_per_request
            )
        )

        self.general_data.recs_with_rats_error = get_only_records_with_specific_error(
            RatsErrorsData.Type.RATS, self.general_data.errors_by_src_system.data
        )
