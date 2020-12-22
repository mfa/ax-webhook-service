import yaml
from google.cloud import datastore

client = datastore.Client()

query = client.query(kind="AX-NLG-Text")
print("All items:")
for item in query.fetch():
    print(item.get("description"), " -- ", item.get("data").get("text")[:70])

print(40 * "-")

# get collections from yml and filter id=12345
collection_data = yaml.load(open("../collections.yml"), Loader=yaml.Loader)
collection_ids = [cid for cid in collection_data.get("collections") if cid != 12345]

for collection in collection_ids:
    query = client.query(kind="AX-NLG-Text")
    query.add_filter("collection_id", "=", collection)

    print(f"All items in collection: {collection}:")
    for item in query.fetch():
        print(item.get("description"), " -- ", item.get("data").get("text")[:70])

        ## delete item after processing:
        # client.delete(item)
