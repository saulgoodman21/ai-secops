from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from fastapi import Query #newly added
import time
import subprocess

app = FastAPI()

class TextIn(BaseModel):
    text: constr(min_length=1, max_length=512)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(item: TextIn):
    # dummy model: positive if length is even
    start = time.time()
    pred = "positive" if len(item.text) % 2 == 0 else "negative"
    return {"label": pred, "score": 0.9, "duration_ms": int((time.time()-start)*1000)}
