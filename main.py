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
        secret = webhook_secrets[document.get("collection_id")]
        signature = req.get_header("X-MYAX-SIGNATURE")
        if not check_signature(signature, data, secret):
            print("CHECK FAILED!", flush=True)

        resp.body = json.dumps(store_document(datastore_client, document))


api = falcon.API()
api.add_route("/", WebhookResource())
