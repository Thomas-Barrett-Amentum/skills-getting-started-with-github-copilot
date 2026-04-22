import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

@pytest.fixture(autouse=True)
def reset_activities():
    # Arrange: Reset the in-memory DB before each test
    for activity in activities.values():
        if isinstance(activity.get("participants"), list):
            activity["participants"] = activity["participants"][:2]  # Reset to initial 2 participants

client = TestClient(app)

def test_get_activities():
    # Arrange: Test client is set up
    # Act: Call the endpoint
    response = client.get("/activities")
    # Assert: Response is OK and contains expected keys
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_success():
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

def test_signup_duplicate():
    # Arrange
    email = activities["Chess Club"]["participants"][0]
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_signup_activity_not_found():
    # Arrange
    email = "ghost@mergington.edu"
    activity = "Nonexistent Club"
    # Act
    response = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
