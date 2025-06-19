def test_list_sources(client):
    resp = client.get("/admin/external-sources")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_add_category(client):
    resp = client.post("/admin/categories", params={"name": "TestCategory", "description": "Test"})
    assert resp.status_code == 200
    assert "Category added" in resp.json().get("message", "")