from src.evidences._base import BaseEvidence
from src.utils.logger import CustomLogger
from src.utils.utils import filter_dict_by_props

logger = CustomLogger(__name__).get_logger()


class EvidenceB(BaseEvidence):
    worksheet_name = "evidence B"

    def get_values(self):
        """
        Get all required data from DB.
        """
        self.values = self.general_data

        src_x_req = filter_dict_by_props(
            self.values.source_per_request, set(self.values.recs_with_lel_segment_empty)
        )

        self.values.assets_with_empty_lel_segment = (
            self.query.get_ps_asset_results_per_src_sys_with_empty_lel_segment(
                src_x_req
            )
        )

    def update_worksheet_with_values(self):
        """
        Provide received date to worksheet as evidences.
        """
        if self.values.assets_with_empty_lel_segment.data:
            self._print_rats_error_parameters()
        else:
            logger.exception("No asset records found for delivery system.")

    def _print_rats_error_parameters(self):
        self.add_query_and_result(
            self.ws["B22"], self.values.assets_with_empty_lel_segment, dict_params={}
        )

    def fetch_required_data(self):
        super().fetch_required_data()
