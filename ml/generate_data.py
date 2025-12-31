import pandas as pd
import numpy as np

np.random.seed(42)

# Generate 5000 data points
n_samples = 5000

# Normal operating conditions (70% of data)
normal_samples = int(n_samples * 0.7)
cpu_normal = np.random.uniform(20, 70, normal_samples)
memory_normal = np.random.uniform(30, 75, normal_samples)
error_rate_normal = np.random.uniform(0.001, 0.05, normal_samples)
latency_normal = np.random.uniform(50, 200, normal_samples)
failed_normal = np.zeros(normal_samples)

# High load but stable (15% of data)
stable_samples = int(n_samples * 0.15)
cpu_stable = np.random.uniform(60, 80, stable_samples)
memory_stable = np.random.uniform(65, 85, stable_samples)
error_rate_stable = np.random.uniform(0.02, 0.07, stable_samples)
latency_stable = np.random.uniform(150, 300, stable_samples)
failed_stable = np.zeros(stable_samples)

# Failure conditions (15% of data)
failure_samples = int(n_samples * 0.15)
cpu_failure = np.random.uniform(75, 100, failure_samples)
memory_failure = np.random.uniform(80, 100, failure_samples)
error_rate_failure = np.random.uniform(0.08, 0.25, failure_samples)
latency_failure = np.random.uniform(300, 800, failure_samples)
failed_failure = np.ones(failure_samples)

# Combine all data
cpu = np.concatenate([cpu_normal, cpu_stable, cpu_failure])
memory = np.concatenate([memory_normal, memory_stable, memory_failure])
error_rate = np.concatenate([error_rate_normal, error_rate_stable, error_rate_failure])
latency = np.concatenate([latency_normal, latency_stable, latency_failure])
failed = np.concatenate([failed_normal, failed_stable, failed_failure])

# Create DataFrame
data = pd.DataFrame({
    'cpu': cpu,
    'memory': memory,
    'error_rate': error_rate,
    'latency': latency,
    'failed': failed.astype(int)
})

# Shuffle the data
data = data.sample(frac=1).reset_index(drop=True)

# Save to CSV
data.to_csv('data.csv', index=False)

print(f"Generated {len(data)} training samples")
print(f"Normal cases: {len(data[data['failed'] == 0])}")
print(f"Failure cases: {len(data[data['failed'] == 1])}")
print("Data saved to data.csv")