import pytest
from model_bakery import baker

from server.models import Category


@pytest.fixture
def category(db):
    return baker.make(Category)


def test_server_endpoint(client, db):
    resp = client.get("/api/server/select/")
    assert resp.status_code == 200


def test_filtering_server_by_category(client, category):
    resp = client.get(f"/api/server/select/?category={category.name}")
    assert resp.status_code == 200


def test_filtering_server_by_category_and_qty(client, category):
    resp = client.get(f"/api/server/select/?category={category.name}&qty=1")
    assert resp.status_code == 200


def test_filtering_server_by_user(client, category):
    resp = client.get("/api/server/select/?by_user=true")
    assert resp.status_code == 200  # Todo Create a user and logged_in_user
