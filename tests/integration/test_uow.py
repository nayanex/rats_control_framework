def test_uow_can_retrieve_ps_import_dataset(sqlite_uow_factory):
    uow = sqlite_uow_factory
    with uow:
        results = list(
            uow.session.execute(
                "SELECT * FROM IPS_OWNER.ps_import_datasets WHERE data_import_type_id = 2"
            )
        )
    import_datasets = [dict(r) for r in results]

    import_dataset_item = {
        "id": 1542,
        "data_import_type_id": 2,
        "log_id": 4857,
        "delivery_timestamp": "01-09-20",
        "status": "FINISHED",
        "progress_message": "LOADEDMDM1631",
    }
    assert_error_msg = "Item not found in ps_import_datasets."
    assert import_dataset_item in import_datasets, assert_error_msg
