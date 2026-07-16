import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.base import Base
from app.db.session import get_db

# Setup in-memory SQLite for isolated API unit testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_document_upload_and_flow():
    # 1. Upload document (POST 202)
    files = {"file": ("manual.pdf", b"Test PDF file content", "application/pdf")}
    res = client.post("/api/documents/upload", files=files)
    assert res.status_code == 202
    data = res.json()
    assert "id" in data
    assert data["status"] == "pending"
    assert data["message"] == "Upload successful, ingestion started."
    doc_id = data["id"]

    # 2. Get document list (GET 200)
    res_list = client.get("/api/documents")
    assert res_list.status_code == 200
    docs = res_list.json()
    assert len(docs) >= 1
    assert docs[0]["id"] == doc_id
    assert docs[0]["filename"] == "manual.pdf"
    assert "upload_date" in docs[0]

    # 3. Get single document details (GET 200)
    res_detail = client.get(f"/api/documents/{doc_id}")
    assert res_detail.status_code == 200
    detail = res_detail.json()
    assert detail["id"] == doc_id
    assert detail["filename"] == "manual.pdf"

    # 4. Get non-existent document (GET 404)
    res_404 = client.get("/api/documents/00000000-0000-0000-0000-000000000000")
    assert res_404.status_code == 404
    err_body = res_404.json()
    assert "error" in err_body
    assert err_body["error"]["code"] == "NOT_FOUND"


def test_query_endpoint():
    # Valid query
    res = client.post("/api/query", json={"query": "Why is valve 101 leaking?", "filters": {}})
    assert res.status_code == 200
    data = res.json()
    assert "answer" in data
    assert "sources" in data
    assert "confidence" in data

    # Empty query (422)
    res_empty = client.post("/api/query", json={"query": "", "filters": {}})
    assert res_empty.status_code == 422
    err_body = res_empty.json()
    assert "error" in err_body
    assert err_body["error"]["code"] in ["UNPROCESSABLE_ENTITY", "INVALID_INPUT"]


def test_graph_neighborhood_endpoint():
    # Valid entity graph query
    res = client.get("/api/graph/neighborhood?entity_id=PUMP-101&depth=1")
    assert res.status_code == 200
    data = res.json()
    assert "nodes" in data
    assert "edges" in data

    # Not found entity (404)
    res_404 = client.get("/api/graph/neighborhood?entity_id=notfound-999")
    assert res_404.status_code == 404
    err_body = res_404.json()
    assert err_body["error"]["code"] == "NOT_FOUND"


def test_alerts_flow():
    # List alerts (GET 200)
    res = client.get("/api/alerts")
    assert res.status_code == 200
    alerts = res.json()
    assert isinstance(alerts, list)

    # Acknowledge non-existent alert (404)
    res_ack_404 = client.post("/api/alerts/00000000-0000-0000-0000-000000000000/acknowledge")
    assert res_ack_404.status_code == 404
    assert res_ack_404.json()["error"]["code"] == "NOT_FOUND"


def test_auth_login_endpoint():
    res = client.post("/api/auth/login", json={"username": "operator", "password": "secretpassword"})
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
