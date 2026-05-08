from fastapi.testclient import TestClient

from app.main import app
from app.schemas import DocumentAnalysis

client = TestClient(app)


def test_empty_text_validation() -> None:
    response = client.post("/api/analyze/text", json={"text": "   "})

    assert response.status_code == 400
    assert "Please provide document text" in response.json()["detail"]


def test_text_analysis_route_uses_mocked_ai(monkeypatch) -> None:
    def fake_analyze_text(text: str) -> DocumentAnalysis:
        assert "lease" in text.lower()
        return DocumentAnalysis(
            document_type="Lease agreement",
            summary="Educational summary.",
            parties=["Tenant", "Landlord"],
            important_dates=["Information not provided."],
            key_obligations=["Review rent payment terms."],
            risks_or_ambiguities=["Late fees may be unclear."],
            possible_outcomes=["Parties may clarify unclear payment language."],
            questions_for_lawyer=["Are the late fee terms enforceable?"],
            source_references=[],
            confidence_notes="Based only on provided text.",
            disclaimer="This is educational document analysis, not legal advice.",
        )

    monkeypatch.setattr("app.api.analyze.analyze_text", fake_analyze_text)

    response = client.post("/api/analyze/text", json={"text": "Lease requires rent."})

    assert response.status_code == 200
    assert response.json()["document_type"] == "Lease agreement"
    assert "not legal advice" in response.json()["disclaimer"]
