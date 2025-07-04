import React, { useState } from "react";
import axios from "axios";

// You can import a Google Font in your index.html or use a CSS-in-JS solution
// For demo, we'll use inline styles and a Google Fonts link in a comment below

function PromptPractice() {
  const [prompt, setPrompt] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Demo prompts for the current challenge
  const goodDemo = "Suggest ways for users to save money on groceries, considering different budgets and dietary needs.";
  const biasedDemo = "Tell single mothers how to save money on groceries."; // Biased: Assumes only single mothers need help.

  const handleCheck = async () => {
    if (!prompt.trim()) return;
    setLoading(true);
    setResult(null);
    try {
      const res = await axios.post("https://safebot-r4i0.onrender.com/check_prompt", { prompt });
      setResult(res.data);
    } catch (error) {
      setResult({ result: "error", reason: "Could not connect to the server." });
    }
    setLoading(false);
  };

  // Styles
  const cardStyle = {
    maxWidth: 480,
    margin: "3em auto",
    padding: "2em",
    background: "#fff",
    borderRadius: "18px",
    boxShadow: "0 4px 24px 0 rgba(0,0,0,0.08)",
    fontFamily: "'Inter', 'Roboto', 'Open Sans', Arial, sans-serif",
  };

  const headingStyle = {
    fontSize: "1.7em",
    fontWeight: 700,
    marginBottom: "0.5em",
    color: "#2d3748",
    textAlign: "center",
    letterSpacing: "0.01em",
  };

  const dividerStyle = {
    border: "none",
    borderTop: "1px solid #e2e8f0",
    margin: "1.5em 0",
  };

  const demoBoxStyle = {
    background: "#f7fafc",
    padding: "1em",
    borderRadius: "10px",
    marginBottom: "1.2em",
    fontSize: "1em",
    color: "#4a5568",
  };

  const textareaStyle = {
    width: "100%",
    padding: "0.8em",
    borderRadius: "8px",
    border: "1px solid #cbd5e1",
    fontSize: "1em",
    marginBottom: "1em",
    fontFamily: "inherit",
    resize: "vertical",
    minHeight: "80px",
  };

  const buttonStyle = {
    padding: "0.7em 2em",
    borderRadius: "8px",
    background: "#3182ce",
    color: "#fff",
    border: "none",
    fontWeight: 600,
    fontSize: "1.1em",
    cursor: loading ? "not-allowed" : "pointer",
    boxShadow: "0 2px 8px 0 rgba(49,130,206,0.08)",
    transition: "background 0.2s",
  };

  const feedbackStyle = result => ({
    marginTop: "1.5em",
    padding: "1.2em",
    borderRadius: "10px",
    background:
      result === "unbiased"
        ? "#e6fffa"
        : result === "biased"
        ? "#fffbea"
        : "#ffe6e6",
    color:
      result === "unbiased"
        ? "#276749"
        : result === "biased"
        ? "#b7791f"
        : "#c53030",
    border:
      result === "unbiased"
        ? "1.5px solid #38b2ac"
        : result === "biased"
        ? "1.5px solid #ecc94b"
        : "1.5px solid #feb2b2",
    fontWeight: 500,
    fontSize: "1.1em",
  });

  // Responsive: stack on mobile
  const responsiveStyle = `
    @media (max-width: 600px) {
      .prompt-card {
        padding: 1em !important;
        margin: 1em !important;
      }
      .prompt-heading {
        font-size: 1.2em !important;
      }
    }
  `;

  return (
    <>
      {/* You can add this to your public/index.html <head> for better font:
      <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
      */}
      <style>{responsiveStyle}</style>
      <div className="prompt-card" style={cardStyle}>
        <div className="prompt-heading" style={headingStyle}>
          🧠 Prompt Practice Code playground
        </div>
        <hr style={dividerStyle} />
        <div style={demoBoxStyle}>
          <div>
            <strong>Example (Good):</strong> {goodDemo}
          </div>
          <div style={{ marginTop: "0.5em" }}>
            <strong>Example (Biased):</strong> {biasedDemo}{" "}
            <em style={{ color: "#b7791f" }}>
              (Biased: Assumes only single mothers need help.)
            </em>
          </div>
        </div>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          placeholder="Write your system prompt here..."
          style={textareaStyle}
        />
        <br />
        <button
          onClick={handleCheck}
          disabled={loading}
          style={buttonStyle}
          onMouseOver={e => (e.target.style.background = "#2563eb")}
          onMouseOut={e => (e.target.style.background = "#3182ce")}
        >
          {loading ? "Checking..." : "Check for Bias"}
        </button>
        {result && (
          <div style={feedbackStyle(result.result)}>
            <strong>
              Result:{" "}
              {result.result === "unbiased"
                ? "✅ Unbiased"
                : result.result === "biased"
                ? "⚠️ Biased"
                : "❌ Error"}
            </strong>
            {result.reason && (
              <div style={{ marginTop: "0.5em" }}>
                <strong>Reason:</strong> {result.reason}
              </div>
            )}
          </div>
        )}
      </div>
    </>
  );
}

export default PromptPractice;
