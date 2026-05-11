import React, { useState } from "react";
import { analyzePdf, analyzeText } from "./api.js";


const DISPLAY_SECTIONS = [
  ["document_type", "Document Type"],
  ["summary", "Summary"],
  ["parties", "Parties"],
  ["important_dates", "Important Dates"],
  ["key_obligations", "Key Obligations"],
  ["risks_or_ambiguities", "Risks or Ambiguities"],
  ["possible_outcomes", "Possible Outcomes"],
  ["questions_for_lawyer", "Questions for a Lawyer"],
  ["confidence_notes", "Confidence Notes"],
  ["disclaimer", "Disclaimer"],
//   ["next_steps", "Next Steps"]
];

function SectionValue({ value }) {
  if (Array.isArray(value)) {
    if (value.length === 0) {
      return <p className="empty-value">No items identified.</p>;
    }

    return (
      <ul>
        {value.map((item, index) => (
          <li key={`${item}-${index}`}>{item}</li>
        ))}
      </ul>
    );
  }

  return <p>{value || "Information not provided."}</p>;
}

function AnalysisResults({ analysis }) {
  if (!analysis) {
    return (
      <section className="placeholder-panel" aria-label="Analysis placeholder">
        <h2>Analysis</h2>
        <p>Your structured document analysis will appear here after you submit text or a PDF.</p>
      </section>
    );
  }

  return (
    <section className="results-panel" aria-label="Structured analysis">
      <h2>Analysis</h2>
      <div className="analysis-grid">
        {DISPLAY_SECTIONS.map(([key, label]) => (
          <article className="analysis-section" key={key}>
            <h3>{label}</h3>
            <SectionValue value={analysis[key]} />
          </article>
        ))}
      </div>
    </section>
  );
}

export default function App() {
  const [text, setText] = useState("");
  const [file, setFile] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function handleAnalyze() {
    setError("");
    setAnalysis(null);

    if (!file && !text.trim()) {
      setError("Paste document text or choose a PDF before analyzing.");
      return;
    }

    setIsLoading(true);

    try {
      const result = file ? await analyzePdf(file) : await analyzeText(text);
      setAnalysis(result);
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <main className="app-shell">
      <section className="intro">
        <p className="eyebrow">Educational document analysis</p>
        <h1>DocuLens AI Legal Document Reader</h1>
        <p>
          Upload a PDF or paste legal-style document text to receive a structured AI-generated
          review of issues, risks, ambiguities, and questions to ask a lawyer.
        </p>
      </section>

      <section className="disclaimer-banner">
        <strong>Not legal advice.</strong> DocuLens provides educational document analysis only. It
        does not predict a legal verdict, guarantee an outcome, or tell you what legal action to
        take.
      </section>

      <section className="workspace">
        <section className="input-panel" aria-label="Document input">
          <div className="field-group">
            <label htmlFor="pdf-upload">PDF upload</label>
            <input
              id="pdf-upload"
              type="file"
              accept="application/pdf"
              onChange={(event) => setFile(event.target.files?.[0] || null)}
            />
          </div>

          <div className="divider">or paste text</div>

          <div className="field-group">
            <label htmlFor="document-text">Document text</label>
            <textarea
              id="document-text"
              value={text}
              onChange={(event) => setText(event.target.value)}
              placeholder="Paste contract, lease, notice, policy, or other legal-style text here..."
              rows={14}
            />
          </div>

          {error ? <div className="error-message">{error}</div> : null}

          <button type="button" onClick={handleAnalyze} disabled={isLoading}>
            {isLoading ? "Analyzing..." : "Analyze Document"}
          </button>
        </section>

        <AnalysisResults analysis={analysis} />
      </section>
    </main>
  );
}
