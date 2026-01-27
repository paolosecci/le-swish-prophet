# Le Swish Prophet Overview
is a web application designed to predict the outcomes of NBA games and outperform Las Vegas sportsbooks. The predictive algorithm uses a dynamically trained ML model, the data mining software uses a web scraper and ETL system, and the site infrastructure runs on a Python server in the Google cloud.

# GCP Deployment Info
## Docker Image in Artifact

Code Language: python:3.12-slim

ID: b792fb85-dd3d-4e16-9576-bfe8ae56551a

CREATE_TIME: 2026-01-27T00:40:16+00:00

SOURCE: gs://le-swish-prophet_cloudbuild/source/1769474407.317541-c7b18731e6ca4991879b19342079c9ee.tgz

IMAGES: us-west2-docker.pkg.dev/le-swish-prophet/lsp-repo/lsp-app:1.0

## Cloud Run
Deployed container to Cloud Run service [le-swish-prophet] in project [le-swish-prophet] region [us-west2]

Service [le-swish-prophet] revision [le-swish-prophet-00001-bir] has been deployed and is serving 100 percent of traffic.

Service URL: https://le-swish-prophet-lag3okfsba-wl.a.run.app
