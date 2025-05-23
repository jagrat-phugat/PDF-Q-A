import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [file, setFile] = useState(null);
  const [docId, setDocId] = useState(null);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [loadingUpload, setLoadingUpload] = useState(false);
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [error, setError] = useState("");

  const upload = async () => {
    if (!file) return setError("Please select a PDF file first!");
    setError("");
    setLoadingUpload(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://localhost:8000/upload/", formData);
      setDocId(res.data.doc_id);
      setAnswer("");
      setQuestion("");
      setError("");
      alert("Uploaded successfully!");
    } catch (err) {
      console.error(err);
      setError("Upload failed! Try again.");
    } finally {
      setLoadingUpload(false);
    }
  };

  const ask = async () => {
    if (!question.trim() || !docId)
      return setError("Please provide both question and upload a file first.");
    setError("");
    setLoadingAnswer(true);
    const formData = new FormData();
    formData.append("doc_id", docId);
    formData.append("question", question);

    try {
      const res = await axios.post("http://localhost:8000/ask/", formData);
      setAnswer(res.data.answer);
      setError("");
    } catch (err) {
      console.error(err);
      setError("Error getting answer. Please try again.");
    } finally {
      setLoadingAnswer(false);
    }
  };

  return (
    <div className="app-container">
      <h1 className="app-title">📄 PDF Q&A Assistant</h1>

      <section className="upload-section card">
        <h2>Upload a PDF</h2>
        <input
          type="file"
          accept="application/pdf"
          onChange={(e) => setFile(e.target.files[0])}
          className="file-input"
        />
        <button
          className={`btn ${loadingUpload ? "btn-loading" : ""}`}
          onClick={upload}
          disabled={loadingUpload}
        >
          {loadingUpload ? "Uploading..." : "Upload"}
        </button>
      </section>

      <section className="ask-section card">
        <h2>Ask a Question</h2>
        <input
          type="text"
          placeholder="Type your question here..."
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          className="question-input"
          disabled={!docId || loadingAnswer}
        />
        <button
          className={`btn ${loadingAnswer ? "btn-loading" : ""}`}
          onClick={ask}
          disabled={loadingAnswer || !docId}
        >
          {loadingAnswer ? "Thinking..." : "Ask"}
        </button>
      </section>

      {error && <div className="error-message">{error}</div>}

      {answer && (
        <section className="answer-section card slide-in">
          <h3>Answer:</h3>
          <p>{answer}</p>
        </section>
      )}
    </div>
  );
}

export default App;
