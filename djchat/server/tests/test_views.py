import pytest
from model_bakery import baker

from server.models import Category, Server
from django.contrib.auth import get_user_model


@pytest.fixture
def user():
    return baker.make(get_user_model())


@pytest.fixture
def logged_in_user(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def category(db):
    return baker.make(Category)


@pytest.fixture
def server(db, category):
    return baker.make(Server, category=category)


def test_server_endpoint(client, db):
    resp = client.get("/api/server/select/")
    assert resp.status_code == 200


def test_filtering_server_by_category(client, category):
    resp = client.get(f"/api/server/select/?category={category.name}")
    assert resp.status_code == 200


def test_filtering_server_by_category_and_qty(client, category):
    resp = client.get(f"/api/server/select/?category={category.name}&qty=1")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_filtering_server_by_user(logged_in_user, category):
    resp = logged_in_user.get("/api/server/select/?by_user=true")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_filtering_server_by_user_not_logged_in(client):
    resp = client.get("/api/server/select/?by_user=true")
    assert resp.status_code == 403
    assert resp.json() == {"detail": "Incorrect authentication credentials."}


def test_filtering_server_by_id(client, server):
    resp = client.get(f"/api/server/select/?by_serverid={server.id}")
    assert resp.status_code == 200


@pytest.mark.django_db
def test_filtering_server_by_id_not_found(client):
    resp = client.get(f"/api/server/select/?by_serverid=99")
    assert resp.status_code == 400
    assert resp.json() == ["Server with id 99 not found"]


@pytest.mark.django_db
def test_filtering_server_by_id_value_error(client):
    resp = client.get(f"/api/server/select/?by_serverid=True")
    assert resp.status_code == 400
    assert resp.json() == ["Server value error"]
