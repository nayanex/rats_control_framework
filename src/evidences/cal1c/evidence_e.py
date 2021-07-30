from src.evidences._base import BaseEvidence
from src.utils.utils import get_last_months_of_upcoming_quarters


class EvidenceE(BaseEvidence):
    worksheet_name = "evidence E"
    colors = {"cc00cc", "00cc00", "ff0000"}

    def get_values(self):
        """
        Get all required data from DB.
        """
        self.values = self.general_data
        alm_dataset_id = self.query.get_alm_import_dataset().data[0]["id"]
        self.values.mortgage_rates = self.query.get_mortgage_rates(
            dataset_id=alm_dataset_id, year=self.year
        )

    def update_worksheet_with_values(self):
        """
        Provide received data to worksheet as evidences
        """
        self._print_mortgage_rates()

    def _print_mortgage_rates(self):
        mortgage_rates = self.values.mortgage_rates
        required_months = get_last_months_of_upcoming_quarters(
            self.quarter, self.year, number=3
        )
        i = 0
        for row in mortgage_rates.data:
            i += 1
            row["value"] = (
                row["value"],
                None
                if (row["year"], row["month"]) not in required_months
                else self.colors.pop(),
            )
            if not self.colors:
                break
        self.ws["B28"] = (
            "The below query is used to fetch the values of 10-year mortgage rates provided by ALM which was imported"
            " in CORE and used in the calculation by RATS"
        )
        self.ws["B30"] = "There are approximately 250 values which change every quarter"
        self.ws[
            "B32"
        ] = "A sample of three proves the correct values were loaded and used for calculation in RatS"
        mortgage_rates.data = mortgage_rates.data[: i + 2]
        self.add_query_and_result(self.ws["B35"], mortgage_rates, {})
