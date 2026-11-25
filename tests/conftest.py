
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from ticket_api.main import app
from ticket_api.database import get_session
from ticket_api import models


@pytest.fixture(name="client")
def client_fixture(tmp_path):
    test_database = tmp_path / "test.db"

    test_engine = create_engine(
        f"sqlite:///{test_database}",
        connect_args={"check_same_thread": False}
    )

    SQLModel.metadata.create_all(test_engine)

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(test_engine)
    test_engine.dispose()
