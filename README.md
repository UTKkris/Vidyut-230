# Project Vidyut-230 MVP

Real-time API for Intent-Aware Anomaly Detection in smart grid telemetry.

## Setup

1. Install dependencies:

pip install -r requirements.txt
Generate baseline grid data:
python data_generator.py

Train the XGBoost model:
python train_model.py

Start the inference API:
python inference_api.py

Testing
Send a simulated meter reading to the API.

curl -X 'POST' \
  'http://localhost:8000/api/v1/ingest' \
  -H 'Content-Type: application/json' \
  -d '{
  "meter_id": "METER-9942",
  "hour": 14,
  "temperature": 38.5,
  "base_load": 140.0,
  "reported_load": 100.0
}'