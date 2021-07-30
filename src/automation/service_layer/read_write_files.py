import csv

import pandas as pd


def generate_dsv_file(dsv_filename, dataset, delimiter):
    """
    Generate dsv file with specified filename.
    :param delimiter: separator character
    :param dataset: data with which to generate csv file from.
    :param dsv_filename: specified csv filename.
    """
    if isinstance(dataset, pd.DataFrame):
        dataset.to_csv(dsv_filename, index=False, sep=delimiter)
    else:
        header_names = dataset[0].keys()
        with open(dsv_filename, "w", newline="") as output_file:
            dict_writer = csv.DictWriter(output_file, header_names, delimiter=delimiter)
            dict_writer.writeheader()
            dict_writer.writerows(dataset)


def generate_txt_file(txt_filename, text_content):
    """
    Generate text file with specified content.
    :param text_content: specified content.
    :param txt_filename: specified text content.
    """
    with open(txt_filename, "w") as f:
        f.write(text_content)
