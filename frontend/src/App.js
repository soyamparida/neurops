import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [cpu, setCpu] = useState("");
  const [memory, setMemory] = useState("");
  const [errorRate, setErrorRate] = useState("");
  const [latency, setLatency] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [systemMetrics, setSystemMetrics] = useState([]);
  const [isAutoMode, setIsAutoMode] = useState(false);
  const [activeTab, setActiveTab] = useState("predict");

  // Fetch alerts and system metrics
  useEffect(() => {
    const fetchData = async () => {
      try {
        const [alertsRes, metricsRes] = await Promise.all([
          axios.get("http://127.0.0.1:8000/alerts"),
          axios.get("http://127.0.0.1:8000/system-metrics")
        ]);
        setAlerts(alertsRes.data);
        setSystemMetrics(metricsRes.data);
      } catch (err) {
        console.log("Error fetching data:", err);
      }
    };
    
    fetchData();
    const interval = setInterval(fetchData, 10000); // Refresh every 10s
    return () => clearInterval(interval);
  }, []);

  // Auto-generate random metrics for demo
  useEffect(() => {
    if (isAutoMode) {
      const interval = setInterval(() => {
        const randomCpu = (Math.random() * 0.8 + 0.1).toFixed(2);
        const randomMemory = (Math.random() * 0.8 + 0.1).toFixed(2);
        const randomError = (Math.random() * 0.1).toFixed(3);
        const randomLatency = Math.floor(Math.random() * 300 + 100);
        
        setCpu(randomCpu);
        setMemory(randomMemory);
        setErrorRate(randomError);
        setLatency(randomLatency);
        
        predictWithValues(randomCpu, randomMemory, randomError, randomLatency);
      }, 3000);
      
      return () => clearInterval(interval);
    }
  }, [isAutoMode]);

  const predictWithValues = async (cpuVal, memVal, errVal, latVal) => {
    try {
      const response = await axios.post("http://127.0.0.1:8000/predict", {
        cpu_load: parseFloat(cpuVal),
        memory_usage: parseFloat(memVal),
        error_rate: parseFloat(errVal),
        latency: parseFloat(latVal)
      });
      const newResult = { ...response.data, timestamp: new Date().toLocaleTimeString() };
      setResult(newResult);
      setHistory(prev => [newResult, ...prev.slice(0, 9)]);
    } catch (err) {
      alert("Backend not running or invalid input");
    }
  };

  const predict = () => predictWithValues(cpu, memory, errorRate, latency);

  const resolveAlert = async (alertId) => {
    try {
      await axios.post(`http://127.0.0.1:8000/alerts/${alertId}/resolve`);
      setAlerts(prev => prev.filter(alert => alert.id !== alertId));
    } catch (err) {
      console.log("Error resolving alert:", err);
    }
  };

  const executeRollback = async () => {
    try {
      await axios.post("http://127.0.0.1:8000/rollback");
      alert("Rollback executed successfully!");
    } catch (err) {
      alert("Error executing rollback");
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>NeurOps</h1>
        <p>AI-Powered DevOps Automation Platform</p>
      </header>

      <nav className="tabs">
        <button 
          className={activeTab === "predict" ? "active" : ""}
          onClick={() => setActiveTab("predict")}
        >
          Predictions
        </button>
        <button 
          className={activeTab === "alerts" ? "active" : ""}
          onClick={() => setActiveTab("alerts")}
        >
          Alerts ({alerts.length})
        </button>
        <button 
          className={activeTab === "metrics" ? "active" : ""}
          onClick={() => setActiveTab("metrics")}
        >
          System Metrics
        </button>
      </nav>

      {activeTab === "predict" && (
        <>
          <section className="description">
            <h2>Deployment Decision System</h2>
            <p>
              Analyzes system metrics to predict deployment risk and automatically decides PROCEED or ROLLBACK.
            </p>
          </section>

          <section className="card">
            <h2>Deployment Metrics</h2>
            <input placeholder="CPU Load (0-1)" value={cpu} onChange={e => setCpu(e.target.value)} />
            <input placeholder="Memory Usage (0-1)" value={memory} onChange={e => setMemory(e.target.value)} />
            <input placeholder="Error Rate (0-1)" value={errorRate} onChange={e => setErrorRate(e.target.value)} />
            <input placeholder="Network Latency (ms)" value={latency} onChange={e => setLatency(e.target.value)} />

            <button onClick={predict}>Predict Decision</button>
            <button 
              onClick={() => setIsAutoMode(!isAutoMode)}
              className={isAutoMode ? "auto-active" : ""}
            >
              {isAutoMode ? "Stop Auto Mode" : "Start Auto Mode"}
            </button>
            <button onClick={executeRollback} className="rollback-btn">
              Execute Manual Rollback
            </button>

            {result && (
              <div className={`result ${result.decision}`}>
                <h3>Decision: {result.decision}</h3>
                <p>Failure Probability: {result.failure_probability}</p>
                <p>Time: {result.timestamp}</p>
              </div>
            )}
          </section>

          {history.length > 0 && (
            <section className="card">
              <h2>Recent Predictions</h2>
              <div className="history">
                {history.map((item, index) => (
                  <div key={index} className={`history-item ${item.decision}`}>
                    <span>{item.timestamp}</span>
                    <span>{item.decision}</span>
                    <span>{item.failure_probability}</span>
                  </div>
                ))}
              </div>
            </section>
          )}
        </>
      )}

      {activeTab === "alerts" && (
        <section className="card">
          <h2>Active Alerts</h2>
          {alerts.length === 0 ? (
            <p>No active alerts</p>
          ) : (
            alerts.map(alert => (
              <div key={alert.id} className={`alert ${alert.severity.toLowerCase()}`}>
                <div className="alert-header">
                  <span className="alert-type">{alert.alert_type}</span>
                  <span className="alert-time">{new Date(alert.timestamp).toLocaleString()}</span>
                </div>
                <p>{alert.message}</p>
                <button onClick={() => resolveAlert(alert.id)}>Resolve</button>
              </div>
            ))
          )}
        </section>
      )}

      {activeTab === "metrics" && (
        <section className="card">
          <h2>System Metrics</h2>
          {systemMetrics.length === 0 ? (
            <p>No metrics available</p>
          ) : (
            <div className="metrics-grid">
              {systemMetrics.slice(0, 5).map((metric, index) => (
                <div key={index} className="metric-item">
                  <div className="metric-time">{new Date(metric.timestamp).toLocaleString()}</div>
                  <div className="metric-values">
                    <div>CPU: {metric.cpu_usage.toFixed(1)}%</div>
                    <div>Memory: {metric.memory_usage.toFixed(1)}%</div>
                    <div>Disk: {metric.disk_usage.toFixed(1)}%</div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </section>
      )}

      <footer>
        Built with FastAPI • React • Machine Learning • Docker • Kubernetes
      </footer>
    </div>
  );
}

export default App;
