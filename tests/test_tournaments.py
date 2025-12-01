import uuid
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session

# NOTE: These imports assume app/main.py and app/database/db.py exist
# and that app/model/models.py contains the Tournament definition.
from app.main import app
from app.database.db import get_session
from app.model.models import Tournament, TournamentStatus

# -------------------------------------------------------
# TEST DATABASE (SQLite in-memory)
# -------------------------------------------------------
# Best practice for testing: use an in-memory database which is faster
# and ensures test isolation by destroying the database after the tests.
test_engine = create_engine(
    "sqlite:///:memory:", connect_args={"check_same_thread": False}
)
# Create all tables in the in-memory database
SQLModel.metadata.create_all(test_engine)


def override_get_session():
    """Overrides the application's get_session dependency to use the test database."""
    with Session(test_engine) as session:
        yield session


# Override the session dependency with the test session
app.dependency_overrides[get_session] = override_get_session

client = TestClient(app)


# -------------------------------------------------------
# TEST 1 — Create Tournament
# -------------------------------------------------------
def test_create_tournament():
    # Explicitly use UTC/Zulu time (Z) in the ISO 8601 strings
    data = {
        "name": "ASTU Champions League",
        "description": "Annual football tournament",
        "status": "planned",
        "logo_url": None,
        "start_date": "2025-01-10T10:00:00Z",  # Updated
        "end_date": "2025-03-10T10:00:00Z",  # Updated
    }

    response = client.post("/tournaments/", json=data)
    assert response.status_code == 200, response.text

    result = response.json()
    assert result["name"] == "ASTU Champions League"
    assert "id" in result
    # The output date string will likely include +00:00 instead of Z, but the date part is correct
    assert "2025-01-10" in result["start_date"]


# -------------------------------------------------------
# TEST 2 — Get All Tournaments
# -------------------------------------------------------
def test_get_all_tournaments():
    # Ensure there's at least one tournament to retrieve
    test_create_tournament()

    response = client.get("/tournaments/")
    assert response.status_code == 200

    tournaments = response.json()
    assert len(tournaments) >= 1


# -------------------------------------------------------
# TEST 3 — Get Tournament by ID
# -------------------------------------------------------
def test_get_tournament_by_id():
    # Create a tournament first
    data = {
        "name": "Engineering Cup",
        "description": "A battle of departments",
        "status": "ongoing",
        "logo_url": None,
        "start_date": "2025-02-01T15:00:00Z",  # Updated
        "end_date": None,
    }

    created = client.post("/tournaments/", json=data).json()
    tournament_id = created["id"]

    # Test GET by ID
    response = client.get(f"/tournaments/{tournament_id}")
    assert response.status_code == 200

    result = response.json()
    assert result["id"] == tournament_id
    assert result["name"] == "Engineering Cup"


# -------------------------------------------------------
# TEST 4 — Update Tournament
# -------------------------------------------------------
def test_update_tournament():
    # Create tournament
    data = {
        "name": "ICT Cup",
        "description": "Tech intramural matches",
        "status": "planned",
        "logo_url": None,
        "start_date": "2025-01-01T12:00:00Z",  # Updated
        "end_date": None,
    }

    created = client.post("/tournaments/", json=data).json()
    tournament_id = created["id"]

    # Update it
    update_data = {
        "name": "ICT Cup Reloaded",
        "description": "Updated description",
        "status": "ongoing",
        "logo_url": None,
        "start_date": "2025-01-02T12:00:00Z",  # Updated
        "end_date": "2025-03-01T12:00:00Z",  # Updated
    }

    response = client.put(f"/tournaments/{tournament_id}", json=update_data)
    assert response.status_code == 200

    updated = response.json()
    assert updated["name"] == "ICT Cup Reloaded"
    assert updated["status"] == "ongoing"


# -------------------------------------------------------
# TEST 5 — Delete Tournament
# -------------------------------------------------------
def test_delete_tournament():
    # Create tournament
    data = {
        "name": "Delete Cup",
        "description": "To be deleted",
        "status": "planned",
        "logo_url": None,
        "start_date": "2025-05-01T10:00:00Z",  # Updated
        "end_date": None,
    }

    created = client.post("/tournaments/", json=data).json()
    tournament_id = created["id"]

    # Delete
    response = client.delete(f"/tournaments/{tournament_id}")
    assert response.status_code == 200

    # Ensure not found
    response = client.get(f"/tournaments/{tournament_id}")
    assert response.status_code == 404
