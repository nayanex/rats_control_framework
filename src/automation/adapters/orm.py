from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Table,
)

metadata = MetaData(schema="ips_owner")

ps_import_datasets = Table(
    "ps_import_datasets",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, index=True, unique=True),
    Column(
        "data_import_type_id",
        ForeignKey("ps_data_import_types.id"),
        nullable=False,
        index=True,
    ),
    Column("log_id", ForeignKey("ps_logs.id"), index=True),
    Column("delivery_timestamp", DateTime, nullable=False),
    Column("status", String(10), nullable=False),
    Column("progress_message", String(4000)),
)

ps_logs = Table(
    "ps_logs",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, index=True),
    Column("creation_timestamp", DateTime, nullable=False),
)

ps_adjustment_sources = Table(
    "ps_adjustment_sources",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("name", String(100), nullable=False, unique=True),
)

ps_adjustment_types = Table(
    "ps_adjustment_types",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column(
        "workflow_type_id",
        ForeignKey("ps_workflow_types.id"),
        nullable=False,
        unique=True,
    ),
    Column("name", String(100), nullable=False, unique=True),
)

ps_workflow_types = Table(
    "ps_workflow_types",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("calculation_type_id", ForeignKey("ps_workflow_types.id")),
    Column("name", String(100), nullable=False, unique=True),
    Column("end_date", DateTime, unique=True),
)

ps_adjustments = Table(
    "ps_adjustments",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, index=True, unique=True),
    Column(
        "adjustment_type_id",
        ForeignKey("ps_adjustment_types.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "adjustment_source_id",
        ForeignKey("ps_adjustment_sources.id"),
        nullable=False,
        index=True,
    ),
    Column("parent_adjustment_id", ForeignKey("ps_adjustments.id")),
    Column("workflow_type", ForeignKey("ps_workflow_types.id")),
    Column("name", String(100), nullable=False),
    Column("value", Numeric(18, 8), nullable=False),
    Column("userid", String(10), nullable=False),
    Column("description", String(4000), nullable=False),
    Column("structural", String(2), nullable=False),
    Column("link_adjustment_id", Integer),
    Column("flow_reason_code", String(50)),
    Column("source_system", String(100)),
    Column("expiry_date", DateTime),
    Column("park_expiry_date", DateTime),
)

ps_audit_trails = Table(
    "ps_audit_trails",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("creation_timestamp", DateTime, nullable=False),
)

ps_calculation_requests = Table(
    "ps_calculation_requests",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False, index=True, unique=True),
    Column(
        "calculation_type_id",
        ForeignKey("ps_calculation_types.id"),
        nullable=False,
        index=True,
    ),
    Column("log_id", ForeignKey("ps_logs.id"), nullable=False, index=True),
    Column(
        "mdl_import_dataset_id",
        ForeignKey("ps_import_datasets.id"),
        index=True,
    ),
    Column(
        "mdm_import_dataset_id",
        ForeignKey("ps_import_datasets.id"),
        index=True,
    ),
    Column(
        "workflow_adjustment_id",
        ForeignKey("ps_workflow_adjustments.id"),
        index=True,
    ),
    Column("increase_import_dataset_id", ForeignKey("ps_import_datasets.id")),
    Column("cif_import_dataset_id", ForeignKey("ps_import_datasets.id")),
    Column("adjustment_id", ForeignKey("ps_adjustments.id")),
    Column("active", String(1), nullable=False),
    Column("status", String(20), nullable=False),
    Column("userid", String(10), nullable=False),
    Column("model_based_flag", Integer, default=0, nullable=False),
    Column("creation_timestamp", DateTime, nullable=False),
    Column("mstr_calc_filter", Integer, default=0),
    Column("ips_import_dataset_id", Integer),
    Column("rsd_import_dataset_id", Integer),
    Column("run_id", Integer),
    Column("linked_calc_req_id", Integer),
    Column("increase_import_dataset_id", Integer),
    Column("description", String(4000)),
    Column("progress_message", String(4000)),
    Column("adj_skip_flag", String(5)),
    Column("rep_status", String(10)),
    Column("flow_reason_code", String(50)),
    Column("source_system", String(100)),
    Column("reporting_period", DateTime),
    Column("completion_timestamp", DateTime),
    Column("cube_refresh_timestamp", DateTime),
)

ps_calculation_types = Table(
    "ps_calculation_types",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("description", String(4000), nullable=False),
)

ps_data_import_types = Table(
    "ps_data_import_types",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("description", String(500), nullable=False),
)

ps_workflow_adjustments = Table(
    "ps_workflow_adjustments",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("workflow_id", ForeignKey("ps_workflows.id"), nullable=False, index=True),
    Column(
        "adjustment_id", ForeignKey("ps_adjustments.id"), nullable=False, unique=True
    ),
    Column(
        "audit_trail_id", ForeignKey("ps_audit_trails.id"), nullable=False, index=True
    ),
    Column("status", String(10), nullable=False),
    Column("calculated_provision", Numeric(18, 5)),
)

ps_workflows = Table(
    "ps_workflows",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column(
        "calculation_request_id",
        ForeignKey("ps_workflows.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "workflow_type_id", ForeignKey("ps_adjustments.id"), nullable=False, index=True
    ),
    Column(
        "audit_trail_id", ForeignKey("ps_audit_trails.id"), nullable=False, index=True
    ),
    Column("status", String(10), nullable=False),
)

ps_data_dictionary = Table(
    "ps_data_dictionary",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column(
        "data_element_type_id",
        ForeignKey("ps_data_element_types.id"),
        nullable=False,
        index=True,
    ),
    Column("code", String(50), nullable=False),
    Column("name", String(200), nullable=False),
    Column("description", String(4000), nullable=False),
    Column("ps_assets_column_name", String(8)),
    Column("ps_asset_results_column_name", String(8)),
    Column("source_id", String(8)),
    Column("end_date", DateTime),
)

ps_calculation_inputs = Table(
    "ps_calculation_inputs",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column(
        "import_dataset_id",
        ForeignKey("ps_import_datasets.id"),
        nullable=False,
        index=True,
    ),
    Column(
        "data_dictionary_id",
        ForeignKey("ps_data_dictionary.id"),
        nullable=False,
        index=True,
    ),
    Column("value", String(4000), nullable=False),
)

ps_data_element_types = Table(
    "ps_data_element_types",
    metadata,
    Column("id", Integer, primary_key=True, index=True, unique=True),
    Column("description", String(500), nullable=False),
)
