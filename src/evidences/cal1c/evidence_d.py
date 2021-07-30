from src.evidences._base import BaseEvidence
from src.utils.utils import get_previous_quarter


class EvidenceD(BaseEvidence):
    worksheet_name = "evidence D"

    SCENARIO_WEIGHT_BASELINE = "RATS_SCENARIO_WEIGHT_BASELINE"
    SCENARIO_WEIGHT_NEGATIVE = "RATS_SCENARIO_WEIGHT_NEGATIVE"
    SCENARIO_WEIGHT_POSITIVE = "RATS_SCENARIO_WEIGHT_POSITIVE"

    code_properties = {
        SCENARIO_WEIGHT_BASELINE: {
            "color_code": "cc00cc",
        },
        SCENARIO_WEIGHT_NEGATIVE: {
            "color_code": "00cc00",
        },
        SCENARIO_WEIGHT_POSITIVE: {
            "color_code": "ff0000",
        },
    }

    def get_values(self):
        """
        Get all required data from DB
        """
        self.values = self.general_data
        self.values.ps_properties = self.query.get_scenario_weights()

    def update_worksheet_with_values(self):
        """
        Provide received data to worksheet as evidences
        """
        self._print_scenario_weights()

    def _print_scenario_weights(self):
        properties = self.values.ps_properties
        for row in properties.data:
            row["property_value"] = (
                row["property_value"],
                self.code_properties.get(row["property_name"])["color_code"],
            )
        previous_run_quarter = get_previous_quarter(self.quarter)
        previous_run_year = self.year - 1 if previous_run_quarter == 4 else self.year
        self.ws[
            "B08"
        ] = "The scenarios to be  used for the calculation by RATS in Q{quarter} {year} will be similar to the ones \
            used in Q{prev_run_quarter} {prev_run_year}".format(
            quarter=self.quarter,
            year=self.year,
            prev_run_quarter=previous_run_quarter,
            prev_run_year=previous_run_year,
        )
        self.ws["B012"] = (
            "Below query on the CORE database production environment (see screenshot) shows the scenario"
            " weightages values which were used in the calculation by RATS for Q{q} 2020.".format(
                q=self.quarter
            )
        )
        self.add_query_and_result(
            self.ws["B15"], properties, dict_params={"bold_columns": ["property_name"]}
        )
