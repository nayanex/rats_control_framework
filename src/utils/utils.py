import datetime


def get_quarter_from_month(month: int) -> int:
    return (month - 1) // 3 + 1


def get_previous_quarter(quarter: int) -> int:
    return (quarter - 1) % 4 or 4


def get_last_months_of_upcoming_quarters(quarter: int, year: int, number: int) -> set:
    result = set()
    for i in range(number):
        y = year + 1 if (quarter + i - 1) // 4 > 0 else year
        m = ((quarter + i) % 4 or 4) * 3
        result.add((y, m))
    return result


def get_month_year_as_string(month: int, year: int, str_format: str) -> str:
    """
    convert month and year to a string representation. For example "Oct 2020"
    """
    date = datetime.date(
        year, month, 1
    )  # get any date of month to convert it to string like "Oct 2020"
    return date.strftime(str_format)


def get_scenario_name(quarter: int, year: int) -> str:
    """"Get scenario name based on information about quarter and year."""
    quarter_month_dict = {1: "FEB", 2: "MAY", 3: "AUG", 4: "NOV"}
    return "{} {} BASE".format(quarter_month_dict[quarter], year)


def get_month_year_str(month: int, year: int):
    return "{month}-{year}".format(month=month, year=year)


def get_quarter_year_str(month: int, year: int):
    return "Q{quarter}_{year}".format(quarter=get_quarter_from_month(month), year=year)


def filter_dict_by_props(old_dict, props):
    """Filters dictionary by given properties."""
    return {curr_key: old_dict[curr_key] for curr_key in props}


def filter_dict_list_by_props(dict_list, *props):
    """Filters list of dictionary by given properties."""
    return list(
        map(lambda curr_dict: filter_dict_by_props(curr_dict, props), dict_list)
    )


def create_dict_list_from_tuple_props(dict_list, key_prop, value_prop):
    """Create list of dictionary with given properties."""
    return [{d[key_prop]: d[value_prop]} for d in dict_list]


def remap_dict_list(dict_list, mapping):
    """Remap a list of dictionary by keys based on mapping instructions."""
    return [
        dict(zip(map(lambda x: mapping[x], d.keys()), d.values())) for d in dict_list
    ]


def merge_list_of_dictionaries(dict_list):
    """"Merge list of dictionaries within single dictionary by combining rows with similar keys into arrays."""
    return {k: [d.get(k) for d in dict_list if k in d] for k in set().union(*dict_list)}


def convert_int_list_to_str(int_list):
    return ", ".join(str(x) for x in int_list)
