import hashlib
import hmac
import json

import pytest
import yaml
from falcon import testing

import main


@pytest.fixture
def collection_id():
    yield 12345


@pytest.fixture
def document(collection_id):
    assert isinstance(collection_id, int)
    yield {
        "id": "52ab6993-3f2e-46f7-b501-4fabdffa7178",
        "uid": "1001",
        "language": "en-GB",
        "collection_id": collection_id,
        "collection_name": "ax webhook example",
        "name": "Product 1001",
        "text": "This is an example text for Product 1001.",
        "text_modified": "2020-12-21T16:59:24.355771+00:00",
        "html": "<p>This is an example text for Product 1001.</p>",
        "html_axite": '<div data-axite-container="1" data-axite-uuid="52ab6993-3f2e-46f7-b501-4fabdffa7178" data-axite-id="44f9cdaf-4ab9-47c9-82c1-fe48bf01644b"><p>This is an example text for Product 1001.</p></div>',
    }


@pytest.fixture
def secret(collection_id):
    yield yaml.load(open("collections.yml"), Loader=yaml.Loader).get("collections").get(
        collection_id
    )


@pytest.fixture
def signature(document, secret):
    assert secret
    digest = hmac.new(
        key=secret.encode(),
        msg=json.dumps(document).encode(),
        digestmod=hashlib.sha1,
    )
    return {
        "X-MYAX-SIGNATURE": f"sha1={digest.hexdigest()}",
        "Content-type": "application/json",
    }


@pytest.fixture()
def client():
    return testing.TestClient(main.api)


def test_get(client):
    doc = {"status": "OK"}

    result = client.simulate_get("/")
    assert result.json == doc


def test_post(client, signature, document):
    result = client.simulate_post("/", headers=signature, json=document)
    r = result.json
    assert r.keys() == {"pk", "collection_id", "uid", "last_update", "description", "data"}
    assert r["data"] == document
    assert r["uid"] == document.get("uid")
    assert r["collection_id"] == document.get("collection_id")
    assert r["pk"].split("|") == [
        str(document.get("collection_id")),
        document.get("uid"),
    ]
