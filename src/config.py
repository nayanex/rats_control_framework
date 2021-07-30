import glob
import os
import pathlib
from os import environ, path

from dotenv import load_dotenv

from src.utils.logger import CustomLogger

PROJECT_ROOT = pathlib.Path(__file__).parent.parent.absolute()
TEMPLATES_DIR = "templates"
OUTPUT_DIR = "output"
MEV_DIR = "mev_files"
MEV_FILE_EXTENSION = "*.txt"
REPORT_EXTENSION = ".xlsx"

load_dotenv(path.join(PROJECT_ROOT, ".env"))
logger = CustomLogger(__name__).get_logger()


def get_oracle_db_uri() -> str:
    """
    Load MPS database environment variables from .env
    :return: string db connection
    """
    host = environ.get("MPS_DB_HOST")
    user = environ.get("MPS_DB_USER")
    password = environ.get("MPS_DB_PASSWORD")
    service_name = environ.get("MPS_DB_SERVICE")
    port = environ.get("MPS_DB_PORT")
    return f"oracle+cx_oracle://{user}:{password}@{host}:{port}/{service_name}"


def get_latest_mev_filename() -> str:
    """
    provides filepath of most recent mev file.
    :return: latest mev filename
    """
    search_path = path.join(PROJECT_ROOT, MEV_DIR, MEV_FILE_EXTENSION)
    mev_file_list = glob.glob(search_path)
    latest_mev_file = max(mev_file_list, key=path.getctime)

    if not path.isfile(latest_mev_file):
        raise FileNotFoundError("File {} doesn't exist".format(latest_mev_file))
    return latest_mev_file


def get_template_filepath(report_name) -> str:
    """
    Get a template filename for chosen report.
    :return: chosen template filename
    """
    template_filepath = path.join(
        PROJECT_ROOT, TEMPLATES_DIR, report_name + REPORT_EXTENSION
    )
    return template_filepath


def get_output_filepath(report_name, time_range) -> str:
    """
    Get a template filename for chosen report.
    :return: chosen template filename
    """
    output_filepath = path.join(
        PROJECT_ROOT, OUTPUT_DIR, report_name + time_range + REPORT_EXTENSION
    )
    return output_filepath


def generate_output_dir(folder_base_name, time_range, data_type_suffix) -> str:
    """
    Create output folder for chosen audit dataset.
    :param data_type_suffix: suffix which indicates dataset type. E.g.: "AAHG"
    :param folder_base_name: base name of the folder.
    :param time_range: period and/or frequency with which dataset is created.
    """
    dir_name = path.join(
        PROJECT_ROOT, OUTPUT_DIR, folder_base_name + data_type_suffix + time_range
    )
    try:
        os.mkdir(dir_name)
    except OSError:
        logger.exception("Creation of the directory {} failed".format(dir_name))
    else:
        logger.info("Successfully created the directory {}.".format(dir_name))
    return dir_name
