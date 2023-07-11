

def test_category_endpoint(client, db):
    resp = client.get("/api/server/select/")
    assert resp.status_code == 200
