import requests
from datetime import datetime, timedelta

NVD_API_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_recent_cves(days_back=7, results_limit=10):
    start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%dT%H:%M:%S.000")
    end_date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000")

    params = {
        "pubStartDate": start_date,
        "pubEndDate": end_date,
        "resultsPerPage": results_limit
    }

    response = requests.get(NVD_API_URL, params=params, timeout=15)
    response.raise_for_status()
    data = response.json()

    cve_summaries = []
    for item in data.get("vulnerabilities", []):
        cve = item["cve"]
        cve_id = cve["id"]
        description = next(
            (d["value"] for d in cve.get("descriptions", []) if d["lang"] == "en"),
            "No description available"
        )
        severity = "Unknown"
        metrics = cve.get("metrics", {})
        if "cvssMetricV31" in metrics:
            severity = metrics["cvssMetricV31"][0]["cvssData"]["baseSeverity"]

        cve_summaries.append({
            "cve_id": cve_id,
            "description": description,
            "severity": severity
        })

    return cve_summaries