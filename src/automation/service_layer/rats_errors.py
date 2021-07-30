from src.utils.utils import (
    create_dict_list_from_tuple_props,
    merge_list_of_dictionaries,
)


def get_only_records_with_specific_error(error_type, errors_by_src_system):
    errors = create_dict_list_from_tuple_props(
        errors_by_src_system, "delivery_system", error_type
    )
    errors = merge_list_of_dictionaries(errors)

    return dict(filter(lambda v: v[1][0] > 0, errors.items()))
