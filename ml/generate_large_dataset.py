import csv
import random

# Set seed for reproducibility
random.seed(42)

# Generate 10,000 data points
data = []
data.append(['cpu', 'memory', 'error_rate', 'latency', 'failed'])

for i in range(10000):
    # Generate different scenarios
    scenario = random.choice(['normal', 'moderate', 'high_load', 'failure'])
    
    if scenario == 'normal':  # 40% normal operations
        cpu = random.uniform(15, 60)
        memory = random.uniform(20, 65)
        error_rate = random.uniform(0.001, 0.04)
        latency = random.uniform(50, 200)
        failed = 0
    elif scenario == 'moderate':  # 30% moderate load
        cpu = random.uniform(50, 75)
        memory = random.uniform(55, 80)
        error_rate = random.uniform(0.02, 0.07)
        latency = random.uniform(150, 300)
        failed = 0 if random.random() > 0.2 else 1  # 20% chance of failure
    elif scenario == 'high_load':  # 20% high load
        cpu = random.uniform(70, 90)
        memory = random.uniform(75, 95)
        error_rate = random.uniform(0.05, 0.12)
        latency = random.uniform(250, 450)
        failed = 1 if random.random() > 0.3 else 0  # 70% chance of failure
    else:  # 10% clear failure conditions
        cpu = random.uniform(85, 100)
        memory = random.uniform(90, 100)
        error_rate = random.uniform(0.10, 0.30)
        latency = random.uniform(400, 800)
        failed = 1
    
    # Add some noise and edge cases
    cpu = max(0, min(100, cpu + random.uniform(-2, 2)))
    memory = max(0, min(100, memory + random.uniform(-2, 2)))
    error_rate = max(0, min(1, error_rate + random.uniform(-0.005, 0.005)))
    latency = max(10, latency + random.uniform(-20, 20))
    
    data.append([round(cpu, 2), round(memory, 2), round(error_rate, 4), round(latency, 1), failed])

# Write to CSV
with open('data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)

print(f"Generated {len(data)-1} training samples")
print("Data distribution:")
print(f"Normal/Success cases: {sum(1 for row in data[1:] if row[4] == 0)}")
print(f"Failure cases: {sum(1 for row in data[1:] if row[4] == 1)}")