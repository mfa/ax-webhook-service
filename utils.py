import hashlib
import hmac

import yaml
from google.cloud import datastore


def check_signature(sig, data, secret):
    try:
        signature_header = sig.replace("sha1=", "")
        signature_content = hmac.new(
            key=secret.encode("utf-8"), msg=data, digestmod=hashlib.sha1
        ).hexdigest()
    except AttributeError:
        pass
    except KeyError:
        pass
    except Exception:
        raise
    else:
        return bool(signature_header == signature_content)
    return False


def store_document(client, document):
    cid = document.get("collection_id")
    uid = document.get("uid")
    language = document.get("language")
    pk = f"{cid}|{uid}"

    if client:
        # Google Datastore
        task_key = client.key("AX-NLG-Text", pk)
        task = datastore.Entity(key=task_key)
        task["description"] = f"collection: {cid}, uid: {uid}, language: {language}"
        task["collection_id"] = cid
        task["uid"] = uid
        task["last_update"] = document.get("text_modified")
        task["data"] = document
        client.put(task)
        print(f"{pk} stored", flush=True)
        return {"status": "OK"}
    else:
        # tests
        return {
            "pk": pk,
            "collection_id": cid,
            "uid": uid,
            "last_update": document.get("text_modified"),
            "description": f"collection: {cid}, uid: {uid}, language: {language}",
            "data": document,
        }
