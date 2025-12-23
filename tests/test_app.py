from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Tennis Club" in data


def test_signup_and_remove_participant():
    activity = "Tennis Club"
    email = "testuser@example.com"

    # Ensure email is not present before test
    resp = client.get("/activities")
    assert resp.status_code == 200
    participants = resp.json()[activity]["participants"]
    if email in participants:
        client.delete(f"/activities/{activity}/participants", params={"email": email})

    # Sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # Verify present
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email in participants

    # Remove participant
    resp = client.delete(f"/activities/{activity}/participants", params={"email": email})
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # Verify removed
    resp = client.get("/activities")
    participants = resp.json()[activity]["participants"]
    assert email not in participants
