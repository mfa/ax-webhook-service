## AX Webhook Service

![Run Tests](https://github.com/mfa/ax-webhook-service/workflows/Run%20Tests/badge.svg)

This is not an official AX Semantics repository!

### about

This Python webservice runs on [Google Cloud Run](https://cloud.google.com/run/) and accepts webhooks from [AX Semantics](https://nlg.ax).  
The texts received by this service are stored in [Google Datastore](https://cloud.google.com/datastore/).


#### Why Google Cloud Run?

- managed by Google
- easy to deploy
- scales up 1000 instances
- cheaper than AWS Fargate and not as complicated as AWS Lambda


#### Why Google Cloud Datastore?

- free tier (20k writes/day; 50k reads/day)
- after that par per 100k read/writes
- no hourly fees (as for PostgreSQL or Redis on Google Cloud)
- using Google Cloud Storage to save the document seems wrong, but directly render a html file and save to Google Cloud Storage as static website maybe a viable option.


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
