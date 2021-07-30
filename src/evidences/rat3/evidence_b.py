import numpy as np

from src.automation.service_layer.outstanding import compute_outstanding_impact
from src.evidences._base import BaseEvidence
from src.utils.logger import CustomLogger
from src.utils.utils import filter_dict_by_props

logger = CustomLogger(__name__).get_logger()

TOTAL_THRESHOLD = 2700000


class EvidenceB(BaseEvidence):
    worksheet_name = "evidence B"

    def get_values(self):
        """
        Get all required data from DB.
        """
        self.values = self.general_data

        src_x_req = filter_dict_by_props(
            self.values.source_per_request, set(self.values.recs_with_rats_error)
        )

        self.values.rats_error_parameters = self.query.get_rats_error_parameters(
            src_x_req
        )

        self.values.principal_outstanding = self.query.get_rats_principal_outstanding(
            src_x_req
        )
        provision_sum_after_adjustment = self.query.get_provision_sum_after_adjustment(
            src_x_req
        )

        self.values.principal_outstanding.data = compute_outstanding_impact(
            self.values.principal_outstanding.data, provision_sum_after_adjustment.data
        )

        self.values.principal_outstanding.query_cmd += (
            "\n ------------------------------------------"
            + provision_sum_after_adjustment.query_cmd
        )

        self.values.total_provision_impact = round(
            np.nansum(
                [
                    item["Applied Flat rates"]
                    for item in self.values.principal_outstanding.data
                ]
            )
        )

    def update_worksheet_with_values(self):
        """
        Provide received date to worksheet as evidences.
        """
        if self.values.rats_error_parameters.data:
            self._print_rats_error_parameters()
        else:
            logger.exception("No rats error parameters found for any delivery system.")

        if self.values.principal_outstanding.data:
            self._print_principal_outstanding()
        else:
            logger.exception("No principal outstanding data found for RATs.")

    def _print_rats_error_parameters(self):
        rats_error_params = self.values.rats_error_parameters
        self.add_query_and_result(self.ws["B15"], rats_error_params, dict_params={})

    def _print_principal_outstanding(self):
        rats_outstanding = self.values.principal_outstanding
        self.add_query_and_result(self.ws["B79"], rats_outstanding, dict_params={})

        is_impact_above_threshold = self.values.total_provision_impact > TOTAL_THRESHOLD

        self.ws[
            "B115"
        ] = "The final impact of not calculating provisions (because of RATS errors) is {} threshold.".format(
            "above" if is_impact_above_threshold else "below"
        )
        self.ws["B108"] = "Total Provisions impact: {}.".format(
            self.values.total_provision_impact
        )
        self.ws["B109"] = "Total Threshold: {}.".format(TOTAL_THRESHOLD)
        self.ws["B110"] = "Total Provisions impact above threshold? {}.".format(
            "yes" if is_impact_above_threshold else "no"
        )

    def fetch_required_data(self):
        super().fetch_required_data()
