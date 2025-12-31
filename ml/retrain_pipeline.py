import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from datetime import datetime

def retrain_model():
    print(f"Starting model retraining at {datetime.now()}")
    
    # Load existing data
    if os.path.exists("data.csv"):
        data = pd.read_csv("data.csv")
    else:
        print("No training data found")
        return
    
    # Generate additional synthetic data to simulate new data
    new_data = pd.DataFrame({
        'cpu': np.random.uniform(20, 95, 100),
        'memory': np.random.uniform(30, 90, 100),
        'error_rate': np.random.uniform(0, 0.15, 100),
        'latency': np.random.uniform(50, 500, 100)
    })
    
    # Create labels based on thresholds
    new_data['failed'] = ((new_data['cpu'] > 80) | 
                         (new_data['memory'] > 85) | 
                         (new_data['error_rate'] > 0.08) | 
                         (new_data['latency'] > 300)).astype(int)
    
    # Combine with existing data
    combined_data = pd.concat([data, new_data], ignore_index=True)
    
    # Features and labels
    X = combined_data.drop('failed', axis=1)
    y = combined_data['failed']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train new model
    model = RandomForestClassifier(n_estimators=150, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    # Evaluate model
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"New model accuracy: {accuracy:.3f}")
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    
    # Save updated model and data
    joblib.dump(model, "model.joblib")
    combined_data.to_csv("data.csv", index=False)
    
    # Save model metadata
    metadata = {
        'timestamp': datetime.now().isoformat(),
        'accuracy': accuracy,
        'training_samples': len(combined_data),
        'model_version': f"v{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    }
    
    with open("model_metadata.txt", "w") as f:
        for key, value in metadata.items():
            f.write(f"{key}: {value}\n")
    
    print("Model retraining completed successfully")
    return accuracy

if __name__ == "__main__":
    retrain_model()