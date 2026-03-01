from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import pandas as pd
import uvicorn

app = FastAPI(title="Project Vidyut-230 API")

with open('vidyut.pkl', 'rb') as f:
    model = pickle.load(f)

class MeterReading(BaseModel):
    meter_id: str
    hour: int
    temperature: float
    base_load: float
    reported_load: float

@app.post("/api/v1/ingest")
def ingest_reading(data: MeterReading):
    features = pd.DataFrame([[data.hour, data.temperature, data.base_load]], 
                            columns=['hour', 'temperature', 'base_load'])
    expected_load = model.predict(features)[0]
    
    loss_gap = expected_load - data.reported_load
    deviation_pct = loss_gap / expected_load
    
    status = "NORMAL"
    action = "LOG_ONLY"
    
    if deviation_pct > 0.08:
        status = "THEFT_DETECTED"
        action = "DISPATCH_FIELD_TEAM"
    elif data.temperature > 35 and deviation_pct > 0.03:
        status = "HIGH_TECHNICAL_LOSS"
        action = "UPDATE_RESISTANCE_MODEL"
        
    return {
        "meter_id": data.meter_id,
        "status": status,
        "action": action,
        "metrics": {
            "expected_load_kw": round(float(expected_load), 2),
            "reported_load_kw": round(data.reported_load, 2),
            "loss_gap_kw": round(float(loss_gap), 2),
            "deviation_pct": round(float(deviation_pct * 100), 2)
        }
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)