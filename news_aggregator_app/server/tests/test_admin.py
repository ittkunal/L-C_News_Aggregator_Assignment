import pytest
from fastapi.testclient import TestClient
from server.main import app
import uuid

client = TestClient(app)

def test_view_external_sources():
    resp = client.get("/admin/external-sources")
    print("DEBUG: external-sources response:", resp.json())
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_add_new_category():
    unique_name = f"science_{uuid.uuid4().hex[:8]}"
    resp = client.post("/admin/categories", params={"name": unique_name, "description": "Science news"})
    print("DEBUG: add category response:", resp.json())
    assert resp.status_code == 200
    assert "added" in resp.json().get("message", "").lower() or "success" in resp.json().get("message", "").lower()

def test_update_external_source():
    resp = client.get("/admin/external-sources")
    sources = resp.json()
    print("DEBUG: sources for update:", sources)
    if sources:
        source_id = sources[0].get("id")
        resp2 = client.put(f"/admin/external-sources/{source_id}", params={"api_key": "NEWKEY123"})
        print("DEBUG: update source response:", resp2.json())
        assert resp2.status_code == 200
        assert "updated" in resp2.json().get("message", "").lower() or "success" in resp2.json().get("message", "").lower()
    else:
        pytest.skip("No external sources to update.")

def test_hide_category():
    resp = client.post("/admin/hide-category", params={"category": "science", "hide": True})
    print("DEBUG: hide category response:", resp.json())
    assert resp.status_code == 200
    assert "hidden" in resp.json().get("message", "").lower() or "success" in resp.json().get("message", "").lower()