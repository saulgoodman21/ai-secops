# import json, sys
# def load_json(path):
#     import json, sys
#     try:
#         with open(path) as f:
#             return json.load(f)
#     except Exception as e:
#         print(f"ERROR: could not read {path}: {e}")
#         # Treat unreadable report as a failure signal
#         print("Gate failed: REPORT_UNREADABLE")
#         sys.exit(1)

# def bandit_summary(path="bandit.json"):
#     try:
#         data = json.load(open(path))
#         results = data.get("results", [])
#         # print a compact summary so you can see what was found in CodeBuild logs
#         print("Bandit findings:",
#               [(r.get("test_id"),
#                 r.get("issue_severity"),
#                 r.get("filename"),
#                 r.get("line_number")) for r in results])
#         return results
#     except Exception as e:
#         print("Could not read bandit.json:", e)
#         return []

# def has_blocking_bandit_findings(results):
#     # Fail on HIGH/CRITICAL, and on specific risky rules regardless of severity
#     BLOCK_RULES = {"B307", "B602", "B603", "B604", "B301", "B303", "B304", "B305"}
#     for r in results:
#         sev = (r.get("issue_severity") or "").lower()
#         rule = r.get("test_id") or ""
#         if sev in {"high", "critical"} or rule in BLOCK_RULES:
#             return True
#     return False

# def has_high_crit_safety(path="safety.json"):
#     try:
#         data = json.load(open(path))
#         # Safety v3 JSON structure: look for severity field if present
#         for vuln in (data if isinstance(data, list) else data.get("vulnerabilities", [])):
#             sev = (vuln.get("severity") or "").lower()
#             if sev in {"high", "critical"}:
#                 return True
#     except Exception as e:
#         print("Could not read safety.json:", e)
#     return False

# def secrets_found(path="secrets.json"):
#     try:
#         # trufflehog json lines; treat non-empty file as a finding
#         with open(path, "r") as f:
#             for line in f:
#                 if line.strip():
#                     return True
#     except Exception as e:
#         print("Could not read secrets.json:", e)
#     return False

# fail = []
# bandit_results = bandit_summary()
# if has_blocking_bandit_findings(bandit_results): fail.append("SAST_HIGH")
# if has_high_crit_safety():                       fail.append("SCA_HIGH")
# if secrets_found():                               fail.append("SECRET_FOUND")

# if fail:
#     print("Gate failed:", ",".join(fail))
#     sys.exit(2)

# print("Gates passed")


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
