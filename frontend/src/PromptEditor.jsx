import { useState, useEffect } from "react";

export default function PromptEditor() {
  const [prompt, setPrompt] = useState("");
  const [status, setStatus] = useState("");

  // Fetch the current prompt on mount
  useEffect(() => {
    fetch("http://localhost:8000/prompt_template.txt")
      .then(res => res.text())
      .then(setPrompt)
      .catch(() => setStatus("Could not load prompt."));
  }, []);

  // Save the prompt to the backend
  const savePrompt = async (e) => {
    e.preventDefault();
    setStatus("Saving...");
    const res = await fetch("http://localhost:8000/update_prompt", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    if (res.ok) {
      setStatus("Prompt updated successfully!");
    } else {
      setStatus("Failed to update prompt.");
    }
  };

  return (
    <div style={{ maxWidth: 600, margin: "2em auto", padding: 20, border: "1px solid #ccc", borderRadius: 8 }}>
      <h2>Edit Chatbot Prompt</h2>
      <form onSubmit={savePrompt}>
        <textarea
          value={prompt}
          onChange={e => setPrompt(e.target.value)}
          rows={18}
          style={{ width: "100%", fontFamily: "monospace", fontSize: 16 }}
        />
        <br />
        <button type="submit" style={{ marginTop: 10 }}>Save Prompt</button>
      </form>
      <div style={{ marginTop: 10, color: "#007700" }}>{status}</div>
    </div>
  );
}
