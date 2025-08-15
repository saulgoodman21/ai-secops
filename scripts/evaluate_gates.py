import json, sys, os

def has_high_crit_bandit():
    try:
        with open("bandit.json") as f:
            data = json.load(f)
        for r in data.get("results", []):
            sev = r.get("issue_severity","").lower()
            if sev in {"high","critical"}:
                return True
    except Exception:
        pass
    return False

def has_high_crit_safety():
    try:
        with open("safety.json") as f:
            data = json.load(f)
        for vuln in data:
            sev = vuln.get("severity","").lower()
            if sev in {"high","critical"}:
                return True
    except Exception:
        pass
    return False

def secrets_found():
    try:
        with open("secrets.json") as f:
            for _ in f:  # any line = a finding
                return True
    except Exception:
        pass
    return False

fail = []
if has_high_crit_bandit(): fail.append("SAST_HIGH")
if has_high_crit_safety(): fail.append("SCA_HIGH")
if secrets_found():         fail.append("SECRET_FOUND")

if fail:
    print("Gate failed:", ",".join(fail))
    sys.exit(2)
print("Gates passed")
