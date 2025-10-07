import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]

def test_signup_and_unregister():
    # Use a unique email for testing
    test_email = "pytestuser@mergington.edu"
    activity = "Chess Club"

    # Ensure not already signed up
    client.post(f"/activities/{activity}/unregister?email={test_email}")

    # Sign up
    resp_signup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_signup.status_code == 200
    assert f"Signed up {test_email}" in resp_signup.json()["message"]

    # Try duplicate signup
    resp_dup = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp_dup.status_code == 400
    assert "already signed up" in resp_dup.json()["detail"]

    # Unregister
    resp_unreg = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp_unreg.status_code == 200
    assert f"Removed {test_email}" in resp_unreg.json()["message"]

    # Try unregistering again
    resp_unreg2 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    assert resp_unreg2.status_code == 400
    assert "not registered" in resp_unreg2.json()["detail"]


def test_signup_invalid_activity():
    resp = client.post("/activities/NonexistentActivity/signup?email=foo@bar.com")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]


def test_unregister_invalid_activity():
    resp = client.post("/activities/NonexistentActivity/unregister?email=foo@bar.com")
    assert resp.status_code == 404
    assert "Activity not found" in resp.json()["detail"]
