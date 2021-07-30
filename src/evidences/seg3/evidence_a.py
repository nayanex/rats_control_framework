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
        if self.values.recs_with_lel_segment_empty:
            self._print_recs_with_lel_segment_empty()
        else:
            logger.exception("No records with empty LEL segments were found.")

    def _print_recs_with_lel_segment_empty(self):
        recs_lel_segment_empty = self.values.errors_by_src_system
        self.add_query_and_result(
            self.ws["B14"], recs_lel_segment_empty, dict_params={}
        )

        self.ws["B36"] = "\n".join(
            [
                "{error_qty} cases for {system} where no Client Segment Lel has been determined.".format(
                    system=source_system,
                    error_qty=self.values.recs_with_lel_segment_empty[source_system],
                )
                for source_system in self.values.recs_with_lel_segment_empty.keys()
            ]
        )

        if self.values.recs_with_lel_segment_empty:
            self.ws["B38"] = "which results in a Zero provision being calculated."
            self.ws[
                "B39"
            ] = "Investigation needed from RATS Team. See SEG#3 Evidence B."

    def fetch_required_data(self):
        super().fetch_required_data()

        self.general_data.errors_by_src_system = (
            self.query.get_rats_errors_per_src_system(
                self.general_data.source_per_request
            )
        )

        self.general_data.recs_with_lel_segment_empty = (
            get_only_records_with_specific_error(
                RatsErrorsData.Type.LEL_SEGMENT_EMPTY,
                self.general_data.errors_by_src_system.data,
            )
        )
