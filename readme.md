## AX Webhook Service

This is not an official AX Semantics repository!

### about

This Python webservice runs on [Google Cloud Run](https://cloud.google.com/run/) and accepts webhooks from [AX Semantics](https://nlg.ax).  
The texts received by this service are stored in [Google Datastore](https://cloud.google.com/datastore/).


#### Why Google Cloud Run?

- managed by Google
- easy to deploy
- scales up 1000 instances
- cheaper than AWS Fargate and not as complicated as AWS Lambda


#### Why use the Falcon Web Framework?

- no other dependencies
- least amount of code


### deployment

add your collection configuration to ``collections.yml``.

needs ``google-cloud-sdk`` in version 321.0 for deployment

```
gcloud beta run deploy ax-webhook --source=. --allow-unauthenticated
```

if successful returns at the end the Service URL:

```
Service [ax-webhook] revision [ax-webhook-00001-abc] has been deployed and is serving 100 percent of traffic.
Service URL: https://ax-webhook-xxxxxxx-ez.a.run.app
```

Add this Service URL as webhook url in to the collection in the AX Semantics system.


### tests

run tests:

```
python -m pytest
```
