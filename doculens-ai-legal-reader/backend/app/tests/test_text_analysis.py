from fastapi.testclient import TestClient

from app.main import app
from app.schemas import DocumentAnalysis


client = TestClient(app)


def test_empty_text_validation() -> None:
    response = client.post("/api/analyze/text", json={"text": "   "})

    assert response.status_code == 400
    assert "Please provide document text" in response.json()["detail"]


def test_text_analysis_uses_mocked_service(monkeypatch) -> None:
    def fake_analyze_document_text(text: str) -> DocumentAnalysis:
        assert "lease agreement" in text
        return DocumentAnalysis(
            document_type="Lease agreement",
            summary="A short educational summary.",
            parties=["Tenant", "Landlord"],
            important_dates=["Information not provided."],
            key_obligations=["Pay rent."],
            risks_or_ambiguities=["Late fee terms are unclear."],
            possible_outcomes=["Parties may need to clarify payment timing."],
            questions_for_lawyer=["Are the late fee terms enforceable in this jurisdiction?"],
            confidence_notes="Based only on the provided text.",
            disclaimer="This is educational document analysis, not legal advice.",
        )

    monkeypatch.setattr("app.api.analyze.analyze_document_text", fake_analyze_document_text)

    response = client.post("/api/analyze/text", json={"text": "This lease agreement requires rent."})

    assert response.status_code == 200
    assert response.json()["document_type"] == "Lease agreement"
    assert "not legal advice" in response.json()["disclaimer"]
