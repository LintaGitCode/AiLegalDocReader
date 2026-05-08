const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function parseApiResponse(response) {
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    throw new Error(data.detail || "Something went wrong. Please try again.");
  }

  return data;
}

export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/api/documents`, {
    method: "POST",
    body: formData,
  });

  return parseApiResponse(response);
}

export async function listDocuments() {
  const response = await fetch(`${API_BASE_URL}/api/documents`);
  return parseApiResponse(response);
}

export async function analyzeText(text) {
  const response = await fetch(`${API_BASE_URL}/api/analyze/text`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });

  return parseApiResponse(response);
}

export async function analyzeDocument(documentId) {
  const response = await fetch(`${API_BASE_URL}/api/analyze/document/${documentId}`, {
    method: "POST",
  });

  return parseApiResponse(response);
}

export async function askQuestion(documentId, question) {
  const response = await fetch(`${API_BASE_URL}/api/questions`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_id: documentId, question }),
  });

  return parseApiResponse(response);
}

export async function compareDocuments(documentIds) {
  const response = await fetch(`${API_BASE_URL}/api/compare`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ document_ids: documentIds }),
  });

  return parseApiResponse(response);
}

export async function getObservabilityEvents() {
  const response = await fetch(`${API_BASE_URL}/api/observability/events`);
  return parseApiResponse(response);
}
