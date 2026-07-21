from app.services.rag_llm_service import fast_model
from app.services.compliance_checklist import ISO_27001_CONTROLS
import time


def check_compliance(document_text):
    results = []

    for control in ISO_27001_CONTROLS:
        prompt = f"""You are a compliance auditor. Given this ISO 27001 control requirement:

Control {control['id']} - {control['name']}: {control['description']}

And this excerpt from a company's security policy document:
---
{document_text[:3000]}
---

Does the document address this control? Answer with exactly one word first
(COVERED, PARTIAL, or MISSING), then a one-sentence explanation."""

        response = fast_model.invoke(prompt)

        if isinstance(response.content, list):
            answer_text = " ".join(str(part) for part in response.content).strip()
        else:
            answer_text = response.content.strip()

        status = "MISSING"
        if answer_text.upper().startswith("COVERED"):
            status = "COVERED"
        elif answer_text.upper().startswith("PARTIAL"):
            status = "PARTIAL"

        results.append({
            "control_id": control["id"],
            "control_name": control["name"],
            "status": status,
            "explanation": answer_text
        })

        time.sleep(13)

    return results