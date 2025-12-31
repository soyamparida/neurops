import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [cpu, setCpu] = useState("");
  const [memory, setMemory] = useState("");
  const [errorRate, setErrorRate] = useState("");
  const [latency, setLatency] = useState("");
  const [result, setResult] = useState(null);

  const predict = async () => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        cpu_load: parseFloat(cpu),
        memory_usage: parseFloat(memory),
        error_rate: parseFloat(errorRate),
        latency: parseFloat(latency)
      });
      setResult(response.data);
    } catch (err) {
      alert("Backend not running or invalid input");
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>NeurOps</h1>
        <p>AI-Powered Deployment Decision System</p>
      </header>

      <section className="description">
        <h2>About the Project</h2>
        <p>
          NeurOps analyzes system metrics (CPU load, memory usage, error rate, and network latency) to predict deployment risk. 
          The system dynamically decides whether a deployment should PROCEED or ROLLBACK.
        </p>
      </section>

      <section className="card">
        <h2>Deployment Metrics</h2>
        <input placeholder="CPU Load (0-1)" value={cpu} onChange={e => setCpu(e.target.value)} />
        <input placeholder="Memory Usage (0-1)" value={memory} onChange={e => setMemory(e.target.value)} />
        <input placeholder="Error Rate (0-1)" value={errorRate} onChange={e => setErrorRate(e.target.value)} />
        <input placeholder="Network Latency (ms)" value={latency} onChange={e => setLatency(e.target.value)} />

        <button onClick={predict}>Predict Decision</button>

        {result && (
          <div className={`result ${result.decision}`}>
            <h3>Decision: {result.decision}</h3>
            <p>Failure Probability: {result.failure_probability}</p>
          </div>
        )}
      </section>

      <footer>
        Built with FastAPI • React • Machine Learning
      </footer>
    </div>
  );
}

export default App;
