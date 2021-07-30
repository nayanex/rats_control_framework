from os import path

from src.automation.data_access_layer.ey_queries import EYQueries
from src.automation.data_transfer_object.rats_controls import EYGeneralData
from src.automation.service_layer.read_write_files import (
    generate_dsv_file,
    generate_txt_file,
)
from src.config import generate_output_dir
from src.evidences.ey.evidence_ey import EvidencesEY
from src.reports._base import BaseReport


class EYReport(BaseReport):
    FILENAME = "EY_Data_Request_Legend_Calc_Ids_"
    report_type = BaseReport.ReportType.QUARTERLY
    evidences = [EvidencesEY]
    report_queries = EYQueries
    general_data = EYGeneralData

    def generate_datasets(self):
        """
        Save EY datasets and respective queries in proper output folder.
        """
        delimiter = "|"
        base_folder_name = "EY_Data_Request"
        time_range = self.get_time_range_str()

        for d_type, d_result in self.general_data.dataset_results.__dict__.items():
            data_type_suffix = "_{}_".format(d_type)
            output_dir = generate_output_dir(
                base_folder_name, time_range, data_type_suffix
            )

            csv_filename = path.join(
                output_dir, time_range + data_type_suffix + "dataset.csv"
            )
            txt_filename = path.join(
                output_dir, time_range + data_type_suffix + "query.txt"
            )

            generate_dsv_file(csv_filename, d_result.data, delimiter)
            generate_txt_file(txt_filename, d_result.query_cmd)
