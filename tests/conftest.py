import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tenacity import retry, stop_after_delay

from src import config
from src.automation.adapters.orm import metadata
from src.automation.data_access_layer import unit_of_work
from tests.prep_test_db import prep_sqlite_test_db


@pytest.fixture
def in_memory_sqlite_db():
    engine = create_engine("sqlite:///:memory:")
    engine.execute("ATTACH DATABASE ':memory:' AS ips_owner;")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def sqlite_session_factory(in_memory_sqlite_db):
    yield sessionmaker(bind=in_memory_sqlite_db)


@pytest.fixture
def sqlite_connection(in_memory_sqlite_db):
    engine = in_memory_sqlite_db
    yield engine.connect()


@retry(stop=stop_after_delay(10))
def wait_for_oracle_db_to_come_up(engine):
    return engine.connect()


@pytest.fixture(scope="session")
def oracle_db():
    engine = create_engine(config.get_oracle_db_uri(), isolation_level="SERIALIZABLE")
    wait_for_oracle_db_to_come_up(engine)
    metadata.create_all(engine)
    return engine


@pytest.fixture
def oracle_session_factory(oracle_db):
    yield sessionmaker(bind=oracle_db)


@pytest.fixture
def oracle_session(oracle_session_factory):
    return oracle_session_factory()


@pytest.fixture
def sqlite_uow_factory(sqlite_connection, sqlite_session_factory):
    prep_sqlite_test_db(sqlite_connection)
    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_connection)
    yield uow
