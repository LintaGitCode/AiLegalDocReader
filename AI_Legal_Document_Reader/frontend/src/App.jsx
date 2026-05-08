import React, { useEffect, useState } from "react";
import {
  analyzeDocument,
  analyzeText,
  askQuestion,
  compareDocuments,
  getObservabilityEvents,
  listDocuments,
  uploadDocument,
} from "./api.js";

const ANALYSIS_SECTIONS = [
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
];

function ValueBlock({ value }) {
  if (Array.isArray(value)) {
    return value.length ? (
      <ul>{value.map((item, index) => <li key={`${item}-${index}`}>{item}</li>)}</ul>
    ) : (
      <p className="muted">No items identified.</p>
    );
  }

  return <p>{value || "Information not provided."}</p>;
}

function Sources({ sources = [] }) {
  if (!sources.length) {
    return null;
  }

  return (
    <section className="sources">
      <h3>Sources</h3>
      {sources.map((source) => (
        <p key={`${source.document_id}-${source.chunk_index}`}>
          <strong>{source.filename}</strong>, page {source.page ?? "unknown"}, chunk{" "}
          {source.chunk_index}: {source.preview}
        </p>
      ))}
    </section>
  );
}

function AnalysisPanel({ result }) {
  if (!result) {
    return <p className="muted">Run an analysis to see structured output here.</p>;
  }

  return (
    <div className="result-stack">
      {ANALYSIS_SECTIONS.map(([key, label]) => (
        <article className="result-section" key={key}>
          <h3>{label}</h3>
          <ValueBlock value={result[key]} />
        </article>
      ))}
      <Sources sources={result.source_references} />
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState("analyze");
  const [documents, setDocuments] = useState([]);
  const [selectedDocumentId, setSelectedDocumentId] = useState("");
  const [selectedCompareIds, setSelectedCompareIds] = useState([]);
  const [file, setFile] = useState(null);
  const [text, setText] = useState("");
  const [question, setQuestion] = useState("");
  const [analysis, setAnalysis] = useState(null);
  const [answer, setAnswer] = useState(null);
  const [comparison, setComparison] = useState(null);
  const [events, setEvents] = useState([]);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function refreshDocuments() {
    const records = await listDocuments();
    setDocuments(records);
    if (!selectedDocumentId && records[0]) {
      setSelectedDocumentId(records[0].document_id);
    }
  }

  useEffect(() => {
    refreshDocuments().catch(() => {});
  }, []);

  async function runAction(action) {
    setError("");
    setIsLoading(true);
    try {
      await action();
    } catch (apiError) {
      setError(apiError.message);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleUploadAndAnalyze() {
    await runAction(async () => {
      if (file) {
        const record = await uploadDocument(file);
        await refreshDocuments();
        setSelectedDocumentId(record.document_id);
        setAnalysis(await analyzeDocument(record.document_id));
      } else if (text.trim()) {
        setAnalysis(await analyzeText(text));
      } else {
        throw new Error("Upload a PDF or paste document text first.");
      }
    });
  }

  async function handleQuestion() {
    await runAction(async () => {
      if (!selectedDocumentId || !question.trim()) {
        throw new Error("Choose an uploaded document and enter a question.");
      }
      setAnswer(await askQuestion(selectedDocumentId, question));
    });
  }

  async function handleCompare() {
    await runAction(async () => {
      if (selectedCompareIds.length < 2) {
        throw new Error("Choose at least two uploaded documents.");
      }
      setComparison(await compareDocuments(selectedCompareIds));
    });
  }

  async function handleLoadEvents() {
    await runAction(async () => {
      setEvents(await getObservabilityEvents());
    });
  }

  function toggleCompareId(documentId) {
    setSelectedCompareIds((current) =>
      current.includes(documentId)
        ? current.filter((id) => id !== documentId)
        : [...current, documentId],
    );
  }

  return (
    <main className="app-shell">
      <section className="hero">
        <p className="eyebrow">LangChain, RAG, and observability preview</p>
        <h1>AI Legal Document Reader</h1>
        <p>
          Upload documents, run educational structured analysis, ask grounded questions, compare
          files, and inspect local observability events.
        </p>
      </section>

      <section className="disclaimer">
        <strong>Not legal advice.</strong> This app provides educational document analysis only. It
        does not predict legal verdicts, guarantee outcomes, or tell you what legal action to take.
      </section>

      <nav className="tabs" aria-label="App sections">
        {["analyze", "qa", "compare", "observability"].map((tab) => (
          <button
            className={activeTab === tab ? "active" : ""}
            key={tab}
            type="button"
            onClick={() => setActiveTab(tab)}
          >
            {tab}
          </button>
        ))}
      </nav>

      {error ? <div className="error-message">{error}</div> : null}

      {activeTab === "analyze" ? (
        <section className="layout">
          <section className="panel">
            <h2>Analyze</h2>
            <label htmlFor="pdf">Upload PDF</label>
            <input id="pdf" type="file" accept="application/pdf" onChange={(event) => setFile(event.target.files?.[0] || null)} />
            <label htmlFor="text">Or Paste Text</label>
            <textarea id="text" rows={12} value={text} onChange={(event) => setText(event.target.value)} />
            <button type="button" onClick={handleUploadAndAnalyze} disabled={isLoading}>
              {isLoading ? "Working..." : "Analyze"}
            </button>
          </section>
          <section className="panel wide">
            <h2>Structured Analysis</h2>
            <AnalysisPanel result={analysis} />
          </section>
        </section>
      ) : null}

      {activeTab === "qa" ? (
        <section className="layout">
          <section className="panel">
            <h2>Ask A Document Question</h2>
            <select value={selectedDocumentId} onChange={(event) => setSelectedDocumentId(event.target.value)}>
              <option value="">Choose a document</option>
              {documents.map((document) => (
                <option key={document.document_id} value={document.document_id}>
                  {document.filename} ({document.chunk_count} chunks)
                </option>
              ))}
            </select>
            <textarea rows={8} value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="What obligations, dates, or ambiguities should be reviewed?" />
            <button type="button" onClick={handleQuestion} disabled={isLoading}>
              {isLoading ? "Retrieving..." : "Ask"}
            </button>
          </section>
          <section className="panel wide">
            <h2>Grounded Answer</h2>
            {answer ? (
              <div className="result-stack">
                <article className="result-section"><h3>Answer</h3><p>{answer.answer}</p></article>
                <article className="result-section"><h3>Issues to Review</h3><ValueBlock value={answer.issues_to_review} /></article>
                <article className="result-section"><h3>Disclaimer</h3><p>{answer.disclaimer}</p></article>
                <Sources sources={answer.source_references} />
              </div>
            ) : <p className="muted">Ask a question about an uploaded PDF.</p>}
          </section>
        </section>
      ) : null}

      {activeTab === "compare" ? (
        <section className="layout">
          <section className="panel">
            <h2>Compare Documents</h2>
            {documents.map((document) => (
              <label className="checkbox-row" key={document.document_id}>
                <input type="checkbox" checked={selectedCompareIds.includes(document.document_id)} onChange={() => toggleCompareId(document.document_id)} />
                {document.filename}
              </label>
            ))}
            <button type="button" onClick={handleCompare} disabled={isLoading}>
              {isLoading ? "Comparing..." : "Compare"}
            </button>
          </section>
          <section className="panel wide">
            <h2>Comparison</h2>
            {comparison ? (
              <div className="result-stack">
                {["summary", "shared_themes", "differences", "conflicting_or_unclear_terms", "questions_for_lawyer", "disclaimer"].map((key) => (
                  <article className="result-section" key={key}>
                    <h3>{key.replaceAll("_", " ")}</h3>
                    <ValueBlock value={comparison[key]} />
                  </article>
                ))}
                <Sources sources={comparison.source_references} />
              </div>
            ) : <p className="muted">Choose two uploaded PDFs to compare.</p>}
          </section>
        </section>
      ) : null}

      {activeTab === "observability" ? (
        <section className="panel">
          <h2>Observability Events</h2>
          <button type="button" onClick={handleLoadEvents} disabled={isLoading}>
            Load Events
          </button>
          <div className="event-list">
            {events.map((event, index) => (
              <pre key={`${event.event_type}-${index}`}>{JSON.stringify(event, null, 2)}</pre>
            ))}
          </div>
        </section>
      ) : null}
    </main>
  );
}
