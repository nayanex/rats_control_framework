import json
import pathlib
from glob import glob
from os import path

import pandas as pd

TESTS_ROOT = pathlib.Path(__file__).parent
TEST_DATA_PATH = path.join(TESTS_ROOT, "data", "*.json")


def prep_sqlite_test_db(conn):
    data = {}
    for data_file in glob(TEST_DATA_PATH):
        with open(data_file) as json_file:
            data.update(json.load(json_file))

    for table_name in data.keys():
        df = pd.DataFrame(data[table_name])
        df.to_sql(table_name, conn, if_exists="append", index=False, schema="ips_owner")
