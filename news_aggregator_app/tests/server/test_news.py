def test_get_headlines(client):
    resp = client.get("/news/headlines")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)

def test_search_articles(client):
    resp = client.get("/news/search", params={"q": "Tesla"})
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)