# Le Swish Prophet Overview
is a web application designed to predict the outcomes of NBA games and outperform Las Vegas sportsbooks. The predictive algorithm uses a dynamically trained ML model, the data mining software uses a web scraper and ETL system, and the site infrastructure runs on serverless architecture in the Google cloud.

---

### https://le-swish-prophet-7sfxstyvyq-wl.a.run.app

---

# GCP Deployment Info
IAM needs "Cloud Build Service Account" permissions to run these

## Configure GCP Project

### 1. to enable required apis:
gcloud services enable run.googleapis.com artifactregistry.googleapis.com cloudbuild.googleapis.com

### 2. to build S3-type Artifact repo to hold docker image:
gcloud artifacts repositories create lsp-repo \
  --repository-format=docker \
  --location=us-west2 \
  --description="Le Swish Prophet images"

## For all redeploys

### 1. to create a docker image artifact from this repo
gcloud builds submit --tag us-west2-docker.pkg.dev/le-swish-prophet-2026/lsp-repo/lsp-app:1.1 .

### 2. to deploy docker image to cloud run
gcloud run deploy le-swish-prophet \
  --image us-west2-docker.pkg.dev/le-swish-prophet-2026/lsp-repo/lsp-app:1.1 \
  --region us-west2 \
  --allow-unauthenticated \
  --port 8080 \
  --timeout 600s
