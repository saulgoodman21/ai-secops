import subprocess, json, sys, os, time

repo = os.environ.get("IMAGE_NAME")
tag  = os.environ.get("CODEBUILD_RESOLVED_SOURCE_VERSION")

def aws(cmd):
    out = subprocess.check_output(["aws"] + cmd, text=True)
    return json.loads(out)

for i in range(30):
    data = aws(["ecr","describe-image-scan-findings",
                "--repository-name", repo,
                "--image-id", f"imageTag={tag}"])
    status = data.get("imageScanStatus",{}).get("status","")
    if status == "COMPLETE":
        findings = data.get("imageScanFindings",{}).get("findingSeverityCounts",{})
        high = findings.get("HIGH",0) + findings.get("CRITICAL",0)
        print("ECR scan findings:", findings)
        if high > 0:
            print("Gate failed: ECR_HIGH")
            sys.exit(3)
        print("ECR scan clean")
        sys.exit(0)
    time.sleep(10)

print("ECR scan timeout, failing safe")
sys.exit(4)
