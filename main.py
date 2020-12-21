import json
import sys

import falcon
import google.auth
import yaml
from google.cloud import datastore

from utils import check_signature, store_document

try:
    datastore_client = datastore.Client()
except google.auth.exceptions.DefaultCredentialsError:
    # for testing
    datastore_client = None

try:
    webhook_secrets = yaml.load(open("collections.yml"), Loader=yaml.Loader).get(
        "collections"
    )
except FileNotFoundError:
    print(
        "copy collections.yml-example to collections.yml and add your collection secrets!"
    )
    sys.exit(1)


class WebhookResource:
    def on_get(self, req, resp):
        resp.body = json.dumps({"status": "OK"})

    def on_post(self, req, resp):
        data = req.bounded_stream.read()
        document = json.loads(data)
        collection_id = document.get("collection_id")
        secret = webhook_secrets[collection_id]
        signature = req.get_header("X-MYAX-SIGNATURE")
        if check_signature(signature, data, secret):
            resp.body = json.dumps(store_document(datastore_client, document))
        else:
            print(f"signature check failed for collection: {collection_id}")
            resp.status = falcon.HTTP_FORBIDDEN


api = falcon.API()
api.add_route("/", WebhookResource())
