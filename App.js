import React, { useState } from "react";
import axios from "axios";

function App() {
  const [feature1, setFeature1] = useState("");
  const [feature2, setFeature2] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        feature1: parseFloat(feature1),
        feature2: parseFloat(feature2)
      });
      setResult(response.data);
    } catch (error) {
      console.error(error);
      setResult({ error: "Something went wrong" });
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "50px" }}>
      <h1>NeuroOps Prediction</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="number"
          step="0.01"
          placeholder="Feature 1"
          value={feature1}
          onChange={(e) => setFeature1(e.target.value)}
          required
        />
        <input
          type="number"
          step="0.01"
          placeholder="Feature 2"
          value={feature2}
          onChange={(e) => setFeature2(e.target.value)}
          required
        />
        <button type="submit">Predict</button>
      </form>

      {result && (
        <div style={{ marginTop: "20px" }}>
          {result.error ? (
            <p>{result.error}</p>
          ) : (
            <p>
              Prediction: {result.prediction} <br />
              Decision: {result.decision}
            </p>
          )}
        </div>
      )}
    </div>
  );
}

export default App;

