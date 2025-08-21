from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, constr
from fastapi import Query #newly added
import time

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

def has_high_crit_bandit():
    try:
        import json
        with open("bandit.json") as f:
            data = json.load(f)
        for r in data.get("results", []):
            sev = r.get("issue_severity","").lower()
            if sev in {"medium","high","critical"}:
                return True
    except Exception:
        pass
    return False
